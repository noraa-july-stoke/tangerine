import json
from tangerine import Tangerine, Router

app = Tangerine('localhost', 8081)
api_router = Router()

# api_router.post('/send-email', lambda ctx:
#     def hello_world():
#         print("hello world")
# )


# calling app.use_router() with a router will append all of the middleware
# contained in that router in order of the routes definition
app.use(api_router)
app.start()
