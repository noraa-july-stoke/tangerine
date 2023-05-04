# ╦ ╦╦ ╦╔═╗╦ ╦
# ╚╦╝║ ║╔═╝║ ║
#  ╩ ╚═╝╚═╝╚═╝
# File: yuzu.py
# Description: This file contains the Auth class which is used to store the
# auth status of a user. This is used to determine if a user is logged in
# or not. And also provides the logic for logging in and out.

from key_lime import KeyLime

class Yuzu:
    def __init__(self, keychain: KeyLime):
        self.keychain = keychain
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

    def authenticate(self, username: str, password: str) -> bool:
        try:
            db = self.client['mydatabase']
            users = db['users']

            query = {'username': username}
            user = users.find_one(query)

            if user and user['password'] == password:
                return True
            else:
                return False

        except Exception as e:
            print(f'Error authenticating user: {e}')
            return False

    def sign_up(self, user_data: dict) -> dict:
        try:
            db = self.client['mydatabase']
            users = db['users']

            result = users.insert_one(user_data)
            print(f'User created with id: {result.inserted_id}')
            user_data['_id'] = str(result.inserted_id)  # Convert ObjectId to string
            return user_data

        except Exception as e:
            print(f'Error creating user: {e}')
            return None

    def login(self, username: str, password: str) -> bool:
        if self.authenticate(username, password):
            try:
                db = self.client['mydatabase']
                users = db['users']

                query = {'username': username}
                user = users.find_one(query)

                if user:
                    self.auth = True
                    self.user = user
                    return True
                else:
                    return False

            except Exception as e:
                print(f'Error logging in user: {e}')
                return False
        else:
            return False

    def logout(self):
        self.auth = False
        self.user = None
