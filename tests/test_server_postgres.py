from tangerine import Tangerine, Ctx, Router
from tangerine.key_lime import KeyLime
from tangerine.yuzu import Yuzu
import json
import jwt
import psycopg2


app = Tangerine()
keychain = KeyLime({
        "SECRET_KEY": "ILOVECATS",
})

def get_user_by_email(email):
    conn = psycopg2.connect("postgresql://postgres:C4melz!!@localhost:5432/local_development")
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
    conn = psycopg2.connect("postgresql://postgres:C4melz!!@localhost:5432/local_development")
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
