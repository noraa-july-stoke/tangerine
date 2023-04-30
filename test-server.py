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
from tangerine import Tangerine, Router, Request, Response, Ctx

app = Tangerine('localhost', 8000)
router = Router()

app.static('/static', 'public')

def hello_world(ctx: Ctx) -> None:
    ctx.body = 'Hello, world!'
    ctx.send(200)


router.get('/hello', hello_world)

app.use_router(router)

app.start()
