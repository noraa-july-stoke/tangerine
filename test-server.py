import json
from tangerine import Tangerine, Router, Ctx

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


#====================================TEST3==============================


app = Tangerine('localhost', 8000, debug_level=2)

# Create main and API routers with debugging enabled
main_router = Router(prefix='/api/main', debug=True)
api_router = Router(prefix='/api', debug=True)

# Serve static files
app.static('^/(?!api).*$', 'public')

# Main router routes
def hello_world_main(ctx: Ctx) -> None:
    ctx.body = 'Hello, world! Main Router'
    ctx.send(200)


main_router.get('/hello', hello_world_main)

# API router routes
def api_hello_world(ctx: Ctx) -> None:
    ctx.body = json.dumps({"message": "Hello from API!"})
    ctx.send(200, content_type='application/json')

api_router.get('/hello', api_hello_world)

# Middleware
def hello_middle(ctx: Ctx) -> None:
    print("Hello from middleware!!!")

app.use(hello_middle)

# Another middleware
def api_version(ctx: Ctx) -> None:
    ctx.set_res_header("X-API-Version", "1.0")

app.use(api_version)

# Use the main and API routers
app.use_router(main_router)
app.use_router(api_router)

# Start the server
app.start()
