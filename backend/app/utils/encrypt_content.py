from base64 import urlsafe_b64encode
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from .derive_key import derive_key  # Import the derive_key function

async def encrypt_content(content: str, password: str) -> str:
    """
    Encrypts the provided content using AES encryption (CFB mode) and the given password.

    :param content: The content to be encrypted.
    :param password: The password to be used for encryption.
    :return: The base64-encoded encrypted content (salt + iv + encrypted content).
    """
    # Generate a random salt and derive the key using the password
    salt = os.urandom(16)
    key = derive_key(password, salt)
    
    # Generate a random IV (Initialization Vector) for AES encryption
    iv = os.urandom(16)
    
    # Create the AES cipher using the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the content
    encrypted = encryptor.update(content.encode()) + encryptor.finalize()
    
    # Return the base64-encoded result of salt + iv + encrypted content
    result = urlsafe_b64encode(salt + iv + encrypted).decode()
    print(result)
    return result
