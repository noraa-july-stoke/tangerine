from tangerine import Tangerine, Ctx, Router
from pymongo import MongoClient
from key_lime import KeyLime
from yuzu import Yuzu
import json

app = Tangerine('localhost', 8000)
client = MongoClient('mongodb://localhost:27017/')

keychain = KeyLime({
    'db_connection_string': 'your_db_connection_string',
    'google_cloud': 'your_google_cloud_key',
    'custom_key': 'your_custom_key_value'
})

# Initialize Yuzu with the keychain
yuzu = Yuzu(keychain)

api_router = Router(prefix='/api')

def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

api_router.get('/hello', api_hello_world)

def signup(ctx: Ctx, yuzu: Yuzu) -> None:
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'username': 'admin',
        'password': 'password'
    }

    created_user = yuzu.sign_up(user_data)
    if created_user:
        ctx.body = json.dumps(created_user)
        ctx.send(201, content_type='application/json')
    else:
        ctx.send(500, content_type='application/json')

api_router.post('/signup', lambda ctx: signup(ctx, yuzu))

def login(ctx: Ctx, yuzu: Yuzu) -> None:
    username = ctx['body'].get('username')
    password = ctx['body'].get('password')

    if yuzu.login(username, password):
        ctx.body = json.dumps({"message": "Logged in successfully"})
        ctx.send(200, content_type='application/json')
    else:
        ctx.body = json.dumps({"message": "Invalid credentials"})
        ctx.send(401, content_type='application/json')

api_router.post('/login', lambda ctx: login(ctx, yuzu))

def logout(ctx: Ctx, yuzu: Yuzu) -> None:
    yuzu.logout()
    ctx.body = json.dumps({"message": "Logged out successfully"})
    ctx.send(200, content_type='application/json')

api_router.post('/logout', lambda ctx: logout(ctx, yuzu))

app.use_router(api_router)

app.start()
