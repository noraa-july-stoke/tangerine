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

TANGERINE DISCORD: https://discord.gg/ABZmtHch

Thanks for checking out Tangerine! This is a new Python framework that I am working on. It is almost to the beta version.
I started writing it because flask didn't support async view functions at the time. They do now as of 2.0 , but still not out of the box. Some of the goals of this framework:

1. To be the easiest python web framework to understand for developers coming from javascript.

2. For the base API to be extremely lightweight and unopinionated, yet also have optional extensions that will work out of the box as you need them. Basically you can boot up an extremely lightweight api to serve static sites within a few minutes, but also there is the option to download plugins that offer a fully-featured CLI, and other tools that would make it work more like ruby on rails or Django. Right now there is an extremely easy to use auth module that allows you to either use a default hashing algorithm or swap out to use your own with just a few lines of code.

3. Support async/await out of the box.

This project does not hit all of these goals in it's current state, but I am working on it. I am posting this here in case there might be any people who are interested in contributing so we can confidently publish a working beta version to PyPi soon. Have a lovely day :)

I am also working on a CLI tool for this.
 Still making skeletons/experimenting with the basic architecture and modules that I want to use.
Current setup work is under branch architecture-setup. There are other repos associated with this:
Bergamot, Buddha's Hand, and Key Limes.


Here are the links to those:
https://github.com/noraa-july-stoke/key-limes
https://github.com/noraa-july-stoke/buddhas-hand


# Commit message keys:

```
I use emojis for commit messages. Here's what they mean:

# for updating any readmes or roadmaps
📖 : <relevant comment>:

# for new features
🚀  : <relevant comment>:

# for debug commits.
🪳👟 : <relevant comment>:

# for refactoring
🧠 : <relevant comment>:

# for documentation
🪷 : <relevant comment>

# branch initialization commit
🌱 : <relevant comment>

# standard merge message
🔀 : <relevant comment>

```

# So far, this is what you can do with tangerine...

## This code boots up a tangerine instance with an api router and some middlewares and authentication setup.

### Example setup for mongodb:

```python
from tangerine import Tangerine, Ctx, Router
from pymongo import MongoClient
from key_lime import KeyLime
from yuzu import Yuzu
import json
import jwt

app = Tangerine()

client = MongoClient('mongodb://localhost:27017/')

keychain = KeyLime({
        "SECRET_KEY": "ILOVECATS",
})

# Initialize Yuzu with the db funcs.

def get_user_by_email(email):
    db = client['mydatabase']
    users = db['users']
    query = {'email': email}
    user = users.find_one(query)
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user

def create_user(user_data):
    db = client['mydatabase']
    users = db['users']
    result = users.insert_one(user_data)
    if result.inserted_id:
        user_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
    return user_data

auth = Yuzu(keychain, get_user_by_email, create_user)

# serve static files to any request not starting with /api
app.static('^/(?!api).*$', './public')

# This is how you define a custom middleware.
def hello_middle(ctx: Ctx, next) -> None:
    print("Hello from middleware!")
    ctx.hello_message = json.dumps({"message": "Hello from middleware!"})
    next()

# ==================== AUTH HANDLERS ====================
def api_hello_world(ctx: Ctx) -> None:
    ctx.body = ctx.hello_message
    ctx.send(200, content_type='application/json')

def signup(ctx: Ctx) -> None:
    user_data = ctx.request.body
    created_user = auth.sign_up(user_data)
    if created_user:
        ctx.body = json.dumps(created_user)
        ctx.send(201, content_type='application/json')
    else:
        ctx.send(500, content_type='application/json')

def login(ctx: Ctx) -> None:
    user_data = ctx.request.body
    email = user_data['email']
    password = user_data['password']
    user_id, token = auth.login(email, password)

    if token:
        ctx.body = json.dumps({"message": "Logged in successfully", "token": token})
        ctx.set_res_header("Set-Cookie", f"auth_token={token}; HttpOnly; Path=/")
        ctx.send(200, content_type='application/json')
        # Set the token as a cookie or in the response headers
    else:
        ctx.body = json.dumps({"message": "Invalid credentials"})
        ctx.send(401, content_type='application/json')

def logout(ctx: Ctx) -> None:
    auth.logout()
    ctx.body = json.dumps({"message": "Logged out successfully"})
    ctx.send(200, content_type='application/json')

@Router.auth_required
def get_protected_content(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "This is protected content. Only authenticated users can see this. I hope you feel special 🍊🍊🍊."})
    ctx.send(200, content_type='application/json')


# ==================== API ROUTES ====================
# if you need to bind more variables to your handler, you can pass in a closure

api_router = Router(prefix='/api')
api_router.post('/logout', logout)
api_router.post('/login', login)
api_router.post('/signup', signup)
api_router.get('/hello', api_hello_world)
# api_router.get('/users', get_and_delete_users)
api_router.get('/protected', get_protected_content)

app.use(hello_middle)
app.use(auth.jwt_middleware)
app.use_router(api_router)
app.start()

```

### example setup for postgres:

```python
from tangerine import Tangerine, Ctx, Router
from key_lime import KeyLime
from yuzu import Yuzu
import json
import jwt
import psycopg2

# ==================== If you don't have schema and tables this part will set that up for you  ====================
conn = psycopg2.connect("postgresql://postgres:<POSTGRESPASSWORD>@localhost:5432/local_development")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create schema if it's not there
cur.execute("""
    CREATE SCHEMA IF NOT EXISTS tangerine;
""")

# Execute a command: this creates a new table named 'users'
cur.execute("""
    CREATE TABLE IF NOT EXISTS tangerine.users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")
# Commit the transaction
conn.commit()
# Close the connection
cur.close()
conn.close()

# =================================================================================================================

app = Tangerine()
keychain = KeyLime({
        "SECRET_KEY": "ILOVECATS",
})


def get_user_by_email(email):
    conn = psycopg2.connect("postgresql://postgres:<POSTGRESPASSWORD>@localhost:5432/local_development")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tangerine.users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return {'_id': user[0], 'email': user[1], 'password': user[2]}
    else:
        return None

def create_user(user_data):
    conn = psycopg2.connect("postgresql://postgres:<POSTGRESPASSWORD>@localhost:5432/local_development")
    cur = conn.cursor()
    cur.execute("INSERT INTO tangerine.users (email, password) VALUES (%s, %s) RETURNING id", (user_data['email'], user_data['password']))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {'_id': user_id, 'email': user_data['email'], 'password': user_data['password']}

auth = Yuzu(keychain, get_user_by_email, create_user)
# serve static files to any request not starting with /api
app.static('^/(?!api).*$', './public')

def signup(ctx: Ctx) -> None:
    user_data = ctx.request.body
    created_user = auth.sign_up(user_data)
    if created_user:
        ctx.body = json.dumps(created_user)
        ctx.send(201, content_type='application/json')
    else:
        ctx.send(500, content_type='application/json')

def login(ctx: Ctx) -> None:
    user_data = ctx.request.body
    email = user_data['email']
    password = user_data['password']
    user_id, token = auth.login(email, password)

    if token:
        ctx.body = json.dumps({"message": "Logged in successfully", "token": token})
        ctx.set_res_header("Set-Cookie", f"auth_token={token}; HttpOnly; Path=/")
        ctx.send(200, content_type='application/json')
    else:
        ctx.body = json.dumps({"message": "Invalid credentials"})
        ctx.send(401, content_type='application/json')

def logout(ctx: Ctx) -> None:
    auth.logout()
    ctx.body = json.dumps({"message": "Logged out successfully"})
    ctx.send(200, content_type='application/json')

@Router.auth_required
def get_protected_content(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "This is protected content. Only authenticated users can see this. I hope you feel special 🍊🍊🍊."})
    ctx.send(200, content_type='application/json')

# ==================== API ROUTES ====================
api_router = Router(prefix='/api')
api_router.post('/logout', logout)
api_router.post('/login', login)
api_router.post('/signup', signup)
api_router.get('/protected', get_protected_content)

app.use(auth.jwt_middleware)
app.use_router(api_router)
app.start()


## More Details TBD


## This readme is a work in progress so keep an eye out for more documentation/outlines of the project.
```
