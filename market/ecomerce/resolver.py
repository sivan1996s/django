
from cryptography.fernet import Fernet
from django.conf import settings
# Create your views here.
import json
def encrypt_token_data(data):
    cipher_suite = Fernet(settings.TOKEN_SECRET_KEY)
    encode_data=json.dumps(data).encode()
    encrypted_data = cipher_suite.encrypt(encode_data).decode()
    # print("encrypted_data",encrypted_data.decode(``))
    return encrypted_data

def decrypt_token_data(data):
    cipher_suite = Fernet(settings.TOKEN_SECRET_KEY)
    encrypted_data = cipher_suite.decrypt(data.encode())
    # print("encrypted_data",encrypted_data.decode())
    return encrypted_data.decode()