from tangerine import Tangerine, Ctx, Router
from pymongo import MongoClient
from tangerine_auth import Yuzu, KeyLime
import json
from tangerine.middleware_extension import cors_middleware

app = Tangerine(debug_level=1)
client = MongoClient('mongodb://localhost:27017/')
keychain = KeyLime({
        "SECRET_KEY": "ILOVECATS",
})

app.use(cors_middleware)
