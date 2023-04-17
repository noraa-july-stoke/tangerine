import json
from tangerine import Tangerine, Router
app = Tangerine('localhost', 8081)
# print(app, "===========APP==========")
router = Router()
# print(router, "===========ROUTER==========")

# app.use(app.static('frontend/'))

router.get('/', lambda ctx: (
    ctx.send('Hello World!'),
    print("route hit")
))

router.get('/hello_world', lambda ctx: (
    ctx.send('Hello World!'),
    print("route hit")
))

# router.post('/', lambda ctx: ctx.send('Hello World!'))
# router.put('/', lambda ctx: ctx.send('Hello World!'))
# router.delete('/', lambda ctx: ctx.send('Hello World!'))

async def get_users(ctx):
    users = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Doe"}
    ]
    ctx.send(json.dumps(users), content_type="application/json")

router.get("/users", get_users)

app.use(router)
app.start()
