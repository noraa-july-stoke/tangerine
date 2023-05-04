# ╦ ╦╦ ╦╔═╗╦ ╦
# ╚╦╝║ ║╔═╝║ ║
#  ╩ ╚═╝╚═╝╚═╝
# File: yuzu.py
# Description: This file contains the Auth class which is used to store the
# auth status of a user. This is used to determine if a user is logged in
# or not. And also provides the logic for logging in and out.
import bcrypt
from key_lime import KeyLime

class Yuzu:
    """
Yuzu:
    A simple authentication system that provides functionality to authenticate users,
    register new users, and log out users.

    Attributes:
        keychain (KeyLime): An instance of the KeyLime class used to access keys and secrets
        required for authentication and other configurations.
        client: An instance of a MongoDB client used to interact with the database.
        auth (bool): A boolean indicating whether the user is authenticated or not.
        user (dict): A dictionary containing the user's information if the user is authenticated, or None otherwise.
    """
    def __init__(self, keychain: KeyLime, client):

        """
        Initializes a new instance of the Yuzu class.

        Args:
            keychain (KeyLime): An instance of the KeyLime class used to access keys and secrets
            required for authentication and other configurations.
            client: An instance of a MongoDB client used to interact with the database.
        """

        self.keychain = keychain
        self.client = client
        self.auth = False
        self.user = None

    def get_config(self, key_name: str) -> str:
        """
        Retrieves a configuration value from the keychain using the key_name parameter.

        Args:
            key_name (str): The name of the configuration to retrieve.

        Returns:
            str: The configuration value retrieved from the keychain.
        """
        return self.keychain.get_key(key_name)

    def setup_database(self):
        """
        Sets up the database connection string and other configurations required to interact with the database.
        """
        # Set up the database using self.db_connection_string
        pass

    def setup_other_configs(self):
        """
        Sets up other configurations, such as Google Cloud configurations, required for the authentication system to function.
        """
        # Set up other configurations using self.google_cloud or other configs from the keychain
        pass

    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticates the user by checking if the provided username and password match a user in the database.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            bool: True if the authentication succeeds, False otherwise.
        """
        try:
            db = self.client['mydatabase']
            users = db['users']

            query = {'username': username}
            user = users.find_one(query)

            if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                return True
            else:
                return False

        except Exception as e:
            print(f'Error authenticating user: {e}')
            return False

    def sign_up(self,user_data: dict) -> dict:
        """
        Creates a new user account by inserting user data into the database.

        Args:
            user_data (dict): A dictionary containing the user's data including username, password and other attributes.

        Returns:
            dict: A dictionary containing the user's data if the user was created successfully, or None otherwise.
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


    def login(self, username: str, password: str) -> bool:
        """
        Logs in a user by authenticating the user and setting the auth and user attributes.

        Args:
            username (str): The username of the user to login.
            password (str): The password of the user to login.

        Returns:
            bool: True if the login succeeds, False otherwise.
        """
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

    def logout(self) -> None:
        """
        Logs a user out by setting the auth and user attributes to False and None respectively.

        Returns:
            None
        """
        self.auth = False
        self.user = None
