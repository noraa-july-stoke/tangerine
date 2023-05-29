from tangerine import Tangerine, Ctx, Router
from pymongo import MongoClient
from tangerine_auth import Yuzu, KeyLime
import json
from tangerine.middleware_extension import cors_middleware

app = Tangerine(debug_level=1)
client = MongoClient('mongodb://localhost:27017/')
keychain = KeyLime({
        "SECRET_KEY": "ILOVECATS",
})
app.use(cors_middleware)

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
    print(ctx.user, "HELLO FROM LOGIN")

    if token:
        ctx.body = json.dumps({"message": "Logged in successfully", "token": token})
        ctx.set_cookie("auth_token", token, HttpOnly=True, samesite=True, Path="/")
        ctx.send(200, content_type='application/json')
        # Set the token as a cookie
    else:
        ctx.body = json.dumps({"message": "Invalid credentials"})
        ctx.send(401, content_type='application/json')


def logout(ctx: Ctx) -> None:
    auth.logout(ctx)
    ctx.body = json.dumps({"message": "Logged out successfully"})
    # Clear the authentication token cookie by setting its value to an empty string and Max-Age to 0
    ctx.set_cookie("auth_token", "", expires="Thu, 01 Jan 1970 00:00:00 GMT", Path="/")
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
