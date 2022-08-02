from dataclasses import dataclass

from ._enc import *


@dataclass
class PrivateKey:
    d: int
    n: int


@dataclass
class PublicKey:
    e: int
    n: int


class RSA:
    def generate_keys(self, keysize: int = 32):
        e, d, N = generateKeys(keysize)
        public_key = f"PublicKey({e}, {N})"
        private_key = f"PrivateKey({d}, {N})"
        return public_key, private_key

    def encrypt_message(self, public_key: str, msg: str):
        key_obj = eval(public_key)
        cipher = encrypt(key_obj.e, key_obj.n, msg)
        return cipher

    def decrypt_message(self, private_key: str, cipher: str):
        key_obj = eval(private_key)
        msg = decrypt(key_obj.d, key_obj.n, cipher)
        return msg
