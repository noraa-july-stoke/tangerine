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

# Initialize Yuzu with the keychain
# Passing client into yuzu allows access to the database.
auth = Yuzu(keychain, client)

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
