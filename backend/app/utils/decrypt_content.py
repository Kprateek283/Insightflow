from base64 import urlsafe_b64decode, urlsafe_b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from app.utils.derive_key import derive_key
import logging

async def decrypt_content(encrypted_data: str, password: str):
    try:
        # Fix padding and decode the encrypted data
        padding = '=' * (4 - len(encrypted_data) % 4)  # Ensure correct padding
        encrypted_data = encrypted_data + padding
        
        # Decode the base64-encoded data
        decoded_data = urlsafe_b64decode(encrypted_data.encode())

        # Extract salt, iv, and ciphertext
        salt = decoded_data[:16]
        iv = decoded_data[16:32]
        ciphertext = decoded_data[32:]

        # Derive the decryption key
        key = derive_key(password, salt)

        # Set up AES cipher
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the content
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        try:
            # Attempt to decode as a UTF-8 string
            return decrypted.decode('utf-8')
        except UnicodeDecodeError:
            # If it's not UTF-8, return base64-encoded binary data
            logging.warning("Decrypted content is binary. Returning base64-encoded binary data.")
            return urlsafe_b64encode(decrypted).decode('utf-8')

    except Exception as e:
        logging.error("Error while decrypting content: %s", str(e), exc_info=True)
        raise ValueError("Incorrect password or corrupt data.")
