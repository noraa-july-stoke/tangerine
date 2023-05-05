# ╦ ╦╦ ╦╔═╗╦ ╦
# ╚╦╝║ ║╔═╝║ ║
#  ╩ ╚═╝╚═╝╚═╝
# File: yuzu.py
# Description: This file contains the Auth class which is used to store the
# auth status of a user. This is used to determine if a user is logged in
# or not. And also provides the logic for logging in and out.
import bcrypt
import datetime
from key_lime import KeyLime
import jwt
from typing import Dict, Tuple
import json


class Yuzu:
    def __init__(self, keychain: KeyLime, client):
        self.keychain = keychain
        self.client = client
        self.auth = False
        self.user = None

    def get_config(self, key_name: str) -> str:
        return self.keychain.get_key(key_name)

    def setup_database(self):
        # Set up the database using self.db_connection_string
        pass

    def setup_other_configs(self):
        # Set up other configurations using self.google_cloud or other configs from the keychain
        pass

    def authenticate(self, email: str, password: str) -> bool:
        try:
            db = self.client['mydatabase']
            users = db['users']

            query = {'email': email}
            user = users.find_one(query)

            if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                return True
            else:
                return False

        except Exception as e:
            print(f'Error authenticating user: {e}')
            return False

    def generate_auth_token(self, user_id: str, email: str) -> str:
        secret_key = self.get_config('JWT')["SECRET_KEY"]
        print("GENERATE AUTH TOKEN VARIABLES", user_id, email, secret_key)
        token_payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(token_payload, secret_key, algorithm='HS256')

    def verify_auth_token(self, token: str) -> dict:
        try:
            secret_key = self.get_config('JWT')["SECRET_KEY"]
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None

    def jwt_middleware(self, ctx) -> None:
        jwt_config = self.get_config("JWT")
        protected_prefixes = jwt_config["PROTECTED_PREFIXES"]
        bypass_allowed = jwt_config["BYPASS_ALLOWED"]

        request_path = ctx.request.path
        if any(request_path.startswith(prefix) for prefix in protected_prefixes) and request_path not in bypass_allowed:
            token = ctx.get_req_header("Authorization")
            print(token, "AUTH HEADER AUTH MIDDLE")

            if not token:
                ctx.body = json.dumps({"message": "Missing token"})
                ctx.send(401, content_type='application/json')
                return

            decoded_token = self.verify_auth_token(token)
            if decoded_token:
                ctx.auth = {
                    'user': decoded_token
                }
            else:
                ctx.body = json.dumps({"message": "Invalid token"})
                ctx.send(401, content_type='application/json')






    def sign_up(self,user_data: dict) -> dict:
        try:
            hashed = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
            user_data['password'] = hashed.decode()  # Convert bytes to string

            db = self.client['mydatabase']
            users = db['users']
            result = users.insert_one(user_data)

            print(f'User created with id: {result.inserted_id}')
            user_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
            return user_data

        except Exception as e:
            print(f'Error creating user: {e}')
            return None



    def login(self, email: str, password: str) -> Tuple[str, str]:
        print(self.authenticate(email, password))
        if self.authenticate(email, password):
            try:
                db = self.client['mydatabase']
                users = db['users']

                query = {'email': email}
                user_data = users.find_one(query)
                print(user_data)

                if user_data:
                    self.auth = True
                    self.user = user_data
                    print(self.user, "SELF.USER")
                    token = self.generate_auth_token(str(user_data["_id"]), email)
                    print(token, "TOKEN!!!!!!!!!!!!!")
                    return str(user_data["_id"]), token
                else:
                    return None, None

            except Exception as e:
                print(f'Error logging in user: {e}')
                return None, None
        else:
            return None, None

    def logout(self):
        self.auth = False
        self.user = None
