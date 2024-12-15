from cryptography.fernet import Fernet


async def get_secret_key() -> bytes:
    key = Fernet.generate_key()
    return key


async def encrypt_data(data: str, key: bytes) -> bytes:
    cipher_suite = Fernet(key=key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


async def decrypt_data(data: bytes, key: bytes) -> str:
    cipher_suite = Fernet(key=key)
    decrypted_data = cipher_suite.decrypt(data)
    return decrypted_data.decode()
