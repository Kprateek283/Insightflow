from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """
    Derives a key from the password using PBKDF2 with SHA-256.

    :param password: The password to derive the key from.
    :param salt: A random salt value to be used in key derivation.
    :param iterations: The number of iterations (default is 100,000).
    :return: The derived key (32 bytes).
    """
    # Create PBKDF2HMAC object to derive the key using SHA-256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the key (256 bits = 32 bytes)
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )

    # Derive the key and return it
    return kdf.derive(password.encode())
