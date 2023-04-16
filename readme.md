# Tangerine


I hate flask so I've decided to make a new python framework with better route creation syntax and
am hoping to tackle some problems such as running database migrations in a better fashion (because
ewwww migrations in python frameworks.... javascript frameworks currently handle this so much better).

This is brand new, so still making skeletons/experimenting with the basic architecture and modules that I want to use.
I am working out some kinks in the Tangerine class before I fixup Request, Response,and Ctx and then start to add in
more functionality. Current setup work is under branch architecture-setup. There are other repos associated with this:
Bergamot, Buddha's Hand, and Key Limes. I am also working on a CLI tool for database migrations.


# Some initial basics...
I am implementing a route creation syntax that I believe is a lot cleaner. It utilizes an lambda function and an endpoint
that get taken in and appended to the router, which can then be passed into the server. I think this could be easier for
javascript developers coming into the python scene.

i was thinking about maybe wrapping the lambdas in a named func under the hood for debugging purposes
and then it would also open the door for allowing an mvc system so you could pick and choose your architecture pattern.
if you pass a lambda in it gets wrapped with a name. if you pass a named function in it gets no wrapper.
so you can do it like this to implement mvc:

```python


from tangerine import Tangerine, Router

def hello_world(ctx):
    ctx.send(200, "Hello, world!")

tangerine = Tangerine()
router = Router()
router.get(Router('/', 'GET', hello_world))

tangerine.use(router.routes())
tangerine.start()

# and using lambda

from tangerine import Tangerine, Router
tangerine = Tangerine()
router = Router()

router.get(Router('/', 'GET', lambda ctx: ctx.send(200, "Hello, world!")))

tangerine.use(router.routes())
tangerine.start()
```


```python
# and then under the hood it goes through this class method if its a lambda
import inspect
# wrap func or not. i am debating whether this is worth it,
# but i think it might offer some convenience.
def wrap_lambda(func):
    if inspect.isfunction(func) and func.__name__ == '<lambda>':
        func_name = f'lambda_{id(func)}'
        wrapped_func = lambda *args, **kwargs: func(*args, **kwargs)
        wrapped_func.__name__ = func_name
        return wrapped_func
    return func
```


```python
# Here is an example implementation of how I intend users be able to start the Tangerine server and begin creating routes. This
# example route sends an email with Tangerine framework:
# I think this syntax is cleaner and easier to work with for developers coming in from javascript
from tangerine import Tangerine, Router
from bergamot import Bergamot

tangerine = Tangerine()
router = Router()

# in reality we'd want to pass in keychain or something to get the email and password
bergamot = Bergamot('youremail@gmail.com', 'yourpassword')

router.post('/send-email', lambda ctx:
    try:
        message = ctx.req.form.get('message')
        recipient = ctx.req.form.get('recipient')

        result = bergamot.send_email(recipient, message)

        ctx.body = result
        ctx.send(200)
    except ValueError as e:
        ctx.body = str(e)
        ctx.send(400)
)
# Use the router with the Tangerine app
tangerine.use(router)

if __name__ == '__main__':
    tangerine.start()


```







# Buddha's hand implemetation ideas

```python
import asyncio
from typing import Dict, Union

from strawberry.asgi import GraphQL
from tortoise import Tortoise
from aioredis import create_redis_pool


class BuddhasHand:
    def __init__(self, db_configs: Dict[str, Dict[str, Union[str, int]]]):
        self.db_configs = db_configs
        self.app = None

    async def setup(self):
        tasks = []
        for db_name, db_config in self.db_configs.items():
            db_type = db_config.get("type")
            if db_type == "tortoise":
                tasks.append(self.connect_tortoise(db_name, db_config))
            elif db_type == "redis":
                tasks.append(self.connect_redis(db_name, db_config))
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
        await asyncio.gather(*tasks)
        from .schema import schema
        self.app = GraphQL(schema)

    async def connect_tortoise(self, db_name: str, db_config: Dict[str, Union[str, int]]):
        await Tortoise.init(
            db_url=db_config.get("conn_string"),
            modules=db_config.get("modules", {}).get(db_name, []),
        )

    async def connect_redis(self, db_name: str, db_config: Dict[str, Union[str, int]]):
        redis = await create_redis_pool(
            db_config.get("conn_string"),
            db=db_config.get("db", 0),
        )
        setattr(self, f"{db_name}_redis", redis)

    async def shutdown(self):
        tasks = []
        for db_name, db_config in self.db_configs.items():
            db_type = db_config.get("type")
            if db_type == "tortoise":
                tasks.append(self.disconnect_tortoise(db_name, db_config))
            elif db_type == "redis":
                tasks.append(self.disconnect_redis(db_name, db_config))
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
        await asyncio.gather(*tasks)

    async def disconnect_tortoise(self, db_name: str, db_config: Dict[str, Union[str, int]]):
        await Tortoise.close_connections()

    async def disconnect_redis(self, db_name: str, db_config: Dict[str, Union[str, int]]):
        redis = getattr(self, f"{db_name}_redis", None)
        if redis:
            redis.close()
            await redis.wait_closed()
            delattr(self, f"{db_name}_redis")
```



### Example usage of Buddha's Hand

```python
from os import environ
from tangerine import Tangerine, Router, Ctx, TangerineError
from key_limes import KeyLimes
from buddhas_hand import BuddhasHand

# Create a dict of database configurations
db_configs = {
    "mongo": {
        "conn_string": environ.get("MONGO_CONN_STRING"),
        "redis_optimization": True,
        "redis_host": environ.get("REDIS_HOST"),
        "redis_port": environ.get("REDIS_PORT"),
        "redis_db": 0
    },
    "postgres": {
        "provider": "tortoise",
        "conn_string": environ.get("POSTGRES_CONN_STRING")
    }
}

# Initialize the BuddhasHand instance with the database configurations
db = BuddhasHand(db_configs)

# Initialize the Tangerine server
tangerine = Tangerine()

# Initialize the KeyLimes keychain
keychain = KeyLimes(
    google_cloud=environ.get("GOOGLE_CLOUD_CREDENTIAL"),
    secret_keys=[environ.get("SECRET_KEY_1"), environ.get("SECRET_KEY_2")],
    db_host=environ.get("DB_HOST"),
    db_conn_string=environ.get("DB_CONN_STRING")
)

# Initialize the Yuzu authentication instance
yuzu = Yuzu(
    strategies={"providers": ["google", "facebook", "twitter", "github"], "local": True},
    keychain=keychain
)

# Set the auth instance of Tangerine to Yuzu
tangerine.auth = yuzu

# Define some routes
router = Router()

@router.get("/")
async def index(ctx: Ctx):
    return {"message": "Hello World!"}

# Mount the router to the Tangerine server
tangerine.use(router)

# Start the server
tangerine.start()


```










## this is just a scratch idea and probably wont be used.
```python
from graphene import ObjectType, String, Int, Schema, List
from buddhas_hand import BuddhasHand

db = BuddhasHand(host="localhost", port=27017, database="mydb")

class Author(ObjectType):
    name = String()
    email = String()

class Post(ObjectType):
    title = String()
    content = String()
    author = Author()

class Query(ObjectType):
    post = Post(title=String())


    async def resolve_post(parent, info, title):
        post = await db.posts.find_one({"title": title})
        author = await db.authors.find_one({"_id": post["author_id"]})
        return Post(title=post["title"], content=post["content"], author=Author(name=author["name"], email=author["email"]))

    posts = List(Post)

    async def resolve_posts(parent, info):
        posts = await db.posts.find().to_list()
        return [Post(title=post["title"], content=post["content"]) for post in posts]

schema = Schema(query=Query)

```

## More Details TBD


## This readme is a work in progress so keep an eye out for more documentation/outlines of the project.
