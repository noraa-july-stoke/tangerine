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
    """
    This class is responsible for handling user authentication, such as
    logging in, logging out, signing up, and generating/verifying tokens.

    Attributes:
    keychain (KeyLime): An instance of KeyLime class, used for retrieving keys.
    client: Database client used for user authentication.
    auth (bool): Authentication status of the user.
    user: Data of the authenticated user.
    """
    def __init__(self, keychain: KeyLime, client):
        """
        Parameters:
        keychain (KeyLime): An instance of KeyLime class, used for retrieving keys.
        client: Database client used for user authentication.
        """
        self.keychain = keychain
        self.client = client
        self.auth = False
        self.user = None

    def get_config(self, key_name: str) -> str:
        """
        Returns the value of the specified key from the keychain.

        Parameters:
        key_name (str): The name of the key.

        Returns:
        str: The value of the key.
        """
        return self.keychain.get_key(key_name)

    def setup_database(self):
        """
        Sets up the database using the database connection string.
        """
        pass

    def setup_other_configs(self):
        """
        Sets up other configurations using the Google Cloud or other configs from the keychain.
        """
        pass

    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticates a user with the provided email and password.

        Parameters:
        email (str): The user's email.
        password (str): The user's password.

        Returns:
        bool: True if the user is authenticated, False otherwise.
        """
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
        """
        Generates an authentication token for a user.

        Parameters:
        user_id (str): The user's ID.
        email (str): The user's email.

        Returns:
        str: The authentication token.
        """
        secret_key = self.get_config('JWT')["SECRET_KEY"]
        print("GENERATE AUTH TOKEN VARIABLES", user_id, email, secret_key)
        token_payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(token_payload, secret_key, algorithm='HS256')

    def verify_auth_token(self, token: str) -> dict:
        """
        Verifies an authentication token.

        Parameters:
        token (str): The authentication token.

        Returns:
        dict: The decoded token if it's valid and not expired, None otherwise.
        """
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
        """
        Middleware to handle JWT authentication.

        Parameters:
        ctx: The context for the request and response.
        """
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
        """
        Signs up a new user.

        Parameters:
        user_data (dict): The user's data.

        Returns:
        dict: The created user's data, None if an error occurred.
        """
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
        """
        Logs in a user with the provided email and password.

        Parameters:
        email (str): The user's email.
        password (str): The user's password.

        Returns:
        Tuple[str, str]: The user's ID and authentication token, (None, None) if an error occurred or the authentication failed.
        """
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
        """
        Logs out the current user.
        """
        self.auth = False
        self.user = None
