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

TANGERINE DISCORD: https://discord.gg/2VsGKfBr

Thanks for checking out Tangerine! This is a new Python framework that I am working on. I hope
it will be a lot more intuitive and easier to use than Flask. I am currently working on the
architecture and basic functionality. I am hoping to have a working full version of the framework
up and running some time soon.

I am also working on a CLI tool for database migrations.
I aim to make the new framework with better route creation syntax than Flask and
am hoping to tackle some problems such as running database migrations in a better fashion (because
ewwww migrations in Python frameworks.... JavaScript frameworks currently handle this so much better).

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
