import base64
from Crypto.Cipher import AES


def aes_encrypt(payload):
    encryption_key = "770A8A65DA156D24EE2A093277530142"
    encryption_key = encryption_key[:16]
    length = 16 - (len(payload) % 16)
    payload += chr(length) * length
    obj = AES.new(encryption_key, AES.MODE_ECB)
    ciphertext = obj.encrypt(payload)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode()


def aes_decrypt(ciphertext):
    encryption_key = "770A8A65DA156D24EE2A093277530142"
    encryption_key = encryption_key[:16]
    obj2 = AES.new(encryption_key, AES.MODE_ECB)
    ciphertext = base64.b64decode(ciphertext)
    plaintext = obj2.decrypt(ciphertext)
    text = plaintext[: -plaintext[-1]]
    text = text.decode()
    return text
