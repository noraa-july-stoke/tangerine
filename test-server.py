# import json
# from tangerine import Tangerine, Router

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
import json
from tangerine import Tangerine, Router, Ctx
app = Tangerine('localhost', 8000, debug=True)
router = Router(True)
apiRouter = Router(True)
app.static('/static', 'public')

def hello_world(ctx: Ctx) -> None:
    ctx.body = 'Hello, world!'
    ctx.send(200)


router.get('/hello', hello_world)


hello_middle = lambda ctx: print("hello world")

app.use(hello_middle)

apiRouter.get('/api/hello', hello_world)

app.use_router(router)
app.use_router(apiRouter)

app.start()
