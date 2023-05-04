
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
# So far, this is what you can do with tangerine...
## This code boots up a tangerine instance with an api router and some middlewares and authentication setup.
I am still looking to clean this up a bit, but this is the general idea of how I want to set up the framework.
```

import json
from tangerine import Tangerine, Ctx, Router
from pymongo import MongoClient
from key_lime import KeyLime
from yuzu import Yuzu
import json

app = Tangerine('localhost', 8000, debug_level=2)
client = MongoClient('mongodb://localhost:27017/')
keychain = KeyLime({
    'db_connection_string': 'your_db_connection_string',
    'google_cloud': 'your_google_cloud_key',
    'custom_key': 'your_custom_key_value',
    "SECRET_KEY": "ILOVECATS"
})
# Initialize Yuzu with the keychain
auth = Yuzu(keychain, client)
app.static('^/(?!api).*$', './public')

# ==================== AUTH HANDLERS ====================
def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

def signup(ctx: Ctx, auth: Yuzu) -> None:
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'username': 'admin',
        'password': 'password'
    }

    created_user = auth.sign_up(user_data)
    if created_user:
        ctx.body = json.dumps(created_user)
        ctx.send(201, content_type='application/json')
    else:
        ctx.send(500, content_type='application/json')


def login(ctx: Ctx, auth: Yuzu) -> None:
    body_str = ctx['body'] # decode bytes to str
    print(body_str)
    body_dict = json.loads(body_str)  # parse str to dict
    username = body_dict.get('username')
    password = body_dict.get('password')

    if auth.login(username, password):
        ctx.body = json.dumps({"message": "Logged in successfully"})
        ctx.send(200, content_type='application/json')
    else:
        ctx.body = json.dumps({"message": "Invalid credentials"})
        ctx.send(401, content_type='application/json')


def logout(ctx: Ctx, yuzu: Yuzu) -> None:
    yuzu.logout()
    ctx.body = json.dumps({"message": "Logged out successfully"})
    ctx.send(200, content_type='application/json')

def get_and_delete_users(ctx: Ctx, client: MongoClient) -> None:
    try:
        # Get all users
        db = client['mydatabase']
        users = db['users']
        all_users = list(users.find())

        # Print all users to console
        for user in all_users:
            print(user)

        # Delete all users
        result = users.delete_many({})
        print(f'{result.deleted_count} users deleted')

        ctx.body = json.dumps({'message': 'All users deleted'})
        ctx.send(200, content_type='application/json')

    except Exception as e:
        print(f'Error getting and deleting users: {e}')
        ctx.send(500, content_type='application/json')


# ==================== API ROUTES ====================
api_router = Router(prefix='/api')
api_router.post('/logout', lambda ctx: logout(ctx, auth))
api_router.post('/login', lambda ctx: login(ctx, auth))
api_router.post('/signup', lambda ctx: signup(ctx, auth))
api_router.get('/hello', api_hello_world)
api_router.get('/users', lambda ctx: get_and_delete_users(ctx, client))


app.use_router(api_router)
app.start()


```

## More Details TBD


## This readme is a work in progress so keep an eye out for more documentation/outlines of the project.
