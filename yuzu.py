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

        # Access the required configurations from the keychain
        self.db_connection_string = self.keychain.get_key('db_connection_string')
        self.google_cloud = self.keychain.get_key('google_cloud')

    def setup_database(self):
        # Set up the database using self.db_connection_string
        pass

    def setup_other_configs(self):
        # Set up other configurations using self.google_cloud or other configs from the keychain
        pass

    def login(self, user):
        # Implement login logic here
        self.auth = True
        self.user = user

    def logout(self):
        self.auth = False
        self.user = None
