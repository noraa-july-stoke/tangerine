from tangerine import Tangerine, Ctx, Router
from pymongo import MongoClient
from key_lime import KeyLime
from yuzu import Yuzu
import json
import jwt

app = Tangerine('localhost', 8000, debug_level=1)
client = MongoClient('mongodb://localhost:27017/')
keychain = KeyLime({
    'db_connection_string': 'your_db_connection_string',
    'google_cloud': 'your_google_cloud_key',
    'custom_key': 'your_custom_key_value',
    "JWT": {
        "SECRET_KEY": "ILOVECATS",
        # Specified which prefixes to protect
        "PROTECTED_PREFIXES": ["/api", "api/v1"],
        # Allows certain entry points for logging in
        "BYPASS_ALLOWED": ["/api/login", "/api/signup", "/api/logout"]
        }
})
# Initialize Yuzu with the keychain
# Passing client into yuzu allows access to the database.
auth = Yuzu(keychain, client)
# serve static files to any request not starting with /api
app.static('^/(?!api).*$', './public')
# ==================== AUTH HANDLERS ====================
def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

def signup(ctx: Ctx, auth: Yuzu) -> None:
    user_data = ctx['body']

    created_user = auth.sign_up(user_data)
    if created_user:
        ctx.body = json.dumps(created_user)
        ctx.send(201, content_type='application/json')
    else:
        ctx.send(500, content_type='application/json')

def login(ctx: Ctx, auth: Yuzu) -> None:
    body_dict = ctx['body']
    email = body_dict.get('email')
    password = body_dict.get('password')
    print(body_dict, "body dict")

    user_id, token = auth.login(email, password)

    if token:
        ctx.auth = auth
        ctx.body = json.dumps({"message": "Logged in successfully", "token": token})
        ctx.send(200, content_type='application/json')
        # Set the token as a cookie or in the response headers
        ctx.set_res_header("Set-Cookie", f"auth_token={token}; HttpOnly; Path=/")
    else:
        ctx.body = json.dumps({"message": "Invalid credentials"})
        ctx.send(401, content_type='application/json')


def logout(ctx: Ctx, auth: Yuzu) -> None:
    auth.logout()
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

def get_protected_content(ctx: Ctx) -> None:
    print(ctx.auth, "ctx.auth")
    if ctx.auth and ctx.auth.get('user'):
        ctx.body = json.dumps({"message": "This is protected content. Only authenticated users can see this. I hope you feel special 🍊🍊🍊."})
        ctx.send(200, content_type='application/json')
    else:
        ctx.body = json.dumps({"message": "Unauthorized"})
        ctx.send(401, content_type='application/json')

# ==================== API ROUTES ====================
# if you need to bind more variables to your handler, you can pass in a closure
api_router = Router(prefix='/api')
api_router.post('/logout', lambda ctx: logout(ctx, auth))
api_router.post('/login', lambda ctx: login(ctx, auth))
api_router.post('/signup', lambda ctx: signup(ctx, auth))
api_router.get('/hello', api_hello_world)
api_router.get('/users', lambda ctx: get_and_delete_users(ctx, client))
api_router.get('/protected', get_protected_content)

# app.use(auth_middleware)
app.use(lambda ctx: auth.jwt_middleware(ctx))
app.use_router(api_router)
app.start()
