
```text
🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊
     ████████╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ ██╗███╗   ██╗███████╗
     ╚══██╔══╝██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗██║████╗  ██║██╔════╝
        ██║   ███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝██║██╔██╗ ██║█████╗
        ██║   ██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗██║██║╚██╗██║██╔══╝
        ██║   ██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║██║██║ ╚████║███████╗
        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊
```
Thanks for checking out Tangerine! This is a new python framework that I am working on. I hope
it will be a lot more intuitive and easier to use than flask. I am currently working on the
architecture and basic functionality. I am hoping to have a working full version of the framework
up and running some time soon.


I am also working on a CLI tool for database migrations.
I aim to make the newframework with better route creation syntax thank flask and
am hoping to tackle some problems such as running database migrations in a better fashion (because
ewwww migrations in python frameworks.... javascript frameworks currently handle this so much better).

This is brand new, so still making skeletons/experimenting with the basic architecture and modules that I want to use.
I am working out some kinks in the Tangerine class before I fixup Request, Response,and Ctx and then start to add in
more functionality. Current setup work is under branch architecture-setup. There are other repos associated with this:
Bergamot, Buddha's Hand, and Key Limes.

# Commit message keys:
```

# anything provided after <relevant comment>: is optional but highly encouraged for tracing.

# for updating any readmes or roadmaps
📖 - <filepath/filename>: <relevant comment>:

# for new features
🚀  - <filepath/filename>: <relevant comment>:

# for debug commits.
🪳👟 - <filepath/filename>: <relevant comment>:

# for refactoring
🧠 - <filepath/filename>: <relevant comment>:

# for documentation
🪷 - <filepath/filename>: <relevant comment>:

# branch initialization commit
🌱 - <filepath/filename>: <relevant comment>

# standard merge message
🔀 - <branch name>: <feature filepath>: <relevant comment>

```
## So far, this is what you can do with tangerine...

```

import json
app = Tangerine('localhost', 8000, debug_level=2)

client = MongoClient('mongodb://localhost:27017/')

main_router = Router(prefix='/api/main')

api_router = Router(prefix='/api')

app.static('^/(?!api).*$', 'public')
def hello_world_main(ctx: Ctx) -> None:
    ctx.body = 'Hello, world! Main Router'
    # print(ctx.to_dict())
    ctx.auth = True
    ctx.send(200)

main_router.get('/hello', hello_world_main)

def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

api_router.get('/hello', api_hello_world)

def hello_middle(ctx: Ctx) -> None:
    print("Hello from middleware!!!")

app.use(hello_middle)

def api_version(ctx: Ctx) -> None:
    ctx.set_res_header("X-API-Version", "1.0")

app.use(api_version)

def create_user(ctx: Ctx) -> None:
    db = client['mydatabase']
    users = db['users']
    body = ctx['body']
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    result = users.insert_one(user_data)
    print(f'User created with id: {result.inserted_id}')
    user_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
    ctx.body = json.dumps(user_data)
    ctx.send(201, content_type='application/json')


def delete_user(ctx: Ctx) -> None:
    db = client['mydatabase']
    users = db['users']
    query = {'name': 'John Doe'}
    result = users.delete_one(query)
    print(f'User deleted, deleted count: {result.deleted_count}')
    ctx.body = json.dumps({"message": f"User deleted, deleted count: {result.deleted_count}"})
    ctx.send(200, content_type='application/json')

api_router.post('/create_user', create_user)
api_router.delete('/delete_user', delete_user)

app.use_router(main_router)
app.use_router(api_router)

app.start()



```

## More Details TBD


## This readme is a work in progress so keep an eye out for more documentation/outlines of the project.
