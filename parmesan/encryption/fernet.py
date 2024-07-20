import base64
import os
from typing import override

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from parmesan.encryption.abc import Encryptor


class FernetEncryptor(Encryptor):
    """Implementation of `Encryptor` using Fernet symmetric encryption."""

    def derive_key(self, master_password: str, salt: bytes) -> bytes:
        """Derive a key from the master password and salt using PBKDF2.

        Args:
            master_password: The master password.
            salt: The salt for key derivation.

        Returns:
            The derived key as bytes.
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    @override
    def encrypt(self, plaintext: str, master_password: str) -> str:
        salt = os.urandom(16)
        key = self.derive_key(master_password, salt)
        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(salt + encrypted_text).decode()

    @override
    def decrypt(self, ciphertext: str, master_password: str) -> str:
        decoded_data = base64.urlsafe_b64decode(ciphertext.encode())
        salt = decoded_data[:16]
        encrypted_text = decoded_data[16:]
        key = self.derive_key(master_password, salt)
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_text).decode()
