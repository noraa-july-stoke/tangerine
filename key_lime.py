#  ╦╔═┌─┐┬ ┬╦  ┬┌┬┐┌─┐
#  ╠╩╗├┤ └┬┘║  ││││├┤
#  ╩ ╩└─┘ ┴ ╩═╝┴┴ ┴└─┘
# File: key_lime.py
# Description: This file contains the KeyLime class which is used to store the
# keychain and encrypt and decrypt messages.
from typing import Dict

class KeyLime:
    def __init__(self, keychain: Dict[str, str] = {}):
        self.keychain = keychain

    def add_key(self, key_name: str, key: str):
        self.keychain[key_name] = key

    def remove_key(self, key_name: str):
        if key_name in self.keychain:
            del self.keychain[key_name]

    def get_key(self, key_name: str) -> str:
        return self.keychain.get(key_name)
