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
