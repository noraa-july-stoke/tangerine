import json
from tangerine import Tangerine, Router, Ctx
from pymongo import MongoClient

#====================================TEST3==============================

# app = Tangerine('localhost', 8081)
# api_router = Router()

# # api_router.post('/send-email', lambda ctx:
# #     def hello_world():
# #         print("hello world")
# # )

# # calling app.use_router() with a router will append all of the middleware
# # contained in that router in order of the routes definition
# app.use(api_router)
# app.start()


#====================================TEST2==============================
# import json
# from tangerine import Tangerine, Router, Ctx
# app = Tangerine('localhost', 8000, debug_level=2)
# router = Router(True)
# apiRouter = Router(True)
# app.static('/static', 'public')

# def hello_world(ctx: Ctx) -> None:
#     ctx.body = 'Hello, world!'
#     ctx.send(200)


# router.get('/hello', hello_world)


# hello_middle = lambda ctx: print("hello world")

# app.use(hello_middle)

# apiRouter.get('/api/hello', hello_world)

# app.use_router(router)
# app.use_router(apiRouter)

# app.start()


#=============================TEST3==============================

app = Tangerine('localhost', 8000, debug_level=2)

client = MongoClient('mongodb://localhost:27017/')

main_router = Router(prefix='/api/main')

api_router = Router(prefix='/api')

app.static('^/(?!api).*$', 'public')
def hello_world_main(ctx: Ctx) -> None:
    ctx.body = 'Hello, world! Main Router'
    # print(ctx.to_dict())
    ctx.auth = True
    ctx.send(200)

main_router.get('/hello', hello_world_main)

def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

api_router.get('/hello', api_hello_world)

def hello_middle(ctx: Ctx) -> None:
    print("Hello from middleware!!!")

app.use(hello_middle)

def api_version(ctx: Ctx) -> None:
    ctx.set_res_header("X-API-Version", "1.0")

app.use(api_version)

def create_user(ctx: Ctx) -> None:
    try:
        db = client['mydatabase']
        users = db['users']
        print('here1')

        body = ctx['body']
        user_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com'
        }

        result = users.insert_one(user_data)
        print(user_data, "USER_DATA=====================")
        print(f'User created with id: {result.inserted_id}')
        user_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
        ctx.body = json.dumps(user_data)
        ctx.send(201, content_type='application/json')
    except Exception as e:
        print(f'Error creating user: {e}')
        ctx.send(500, content_type='application/json')



def delete_user(ctx: Ctx) -> None:
    db = client['mydatabase']
    users = db['users']
    query = {'name': 'John Doe'}
    result = users.delete_one(query)
    print(f'User deleted, deleted count: {result.deleted_count}')
    ctx.body = json.dumps({"message": f"User deleted, deleted count: {result.deleted_count}"})
    ctx.send(200, content_type='application/json')

api_router.post('/create_user', create_user)
api_router.delete('/delete_user', delete_user)

app.use_router(main_router)
app.use_router(api_router)

app.start()
