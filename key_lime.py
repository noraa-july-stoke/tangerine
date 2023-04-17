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
