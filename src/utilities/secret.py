import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv  # noqa: F401

key = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(key)


async def encrypt_data(data: str) -> bytes:
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


async def decrypt_data(data: bytes) -> str:
    decrypted_data = cipher_suite.decrypt(data)
    return decrypted_data.decode()
