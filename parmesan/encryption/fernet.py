import base64
import os
from functools import lru_cache
from typing import override

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from parmesan.encryption.abc import Encryptor
from parmesan.encryption.errors import IncorrectMasterPasswordError


class FernetEncryptor(Encryptor):
    """Implementation of `Encryptor` using Fernet symmetric encryption."""

    SALT_SIZE = 16

    @staticmethod
    @lru_cache
    def derive_key(master_password: str, salt: bytes, iterations: int = 100_000) -> bytes:
        """Derive a key from the master password and salt using PBKDF2.

        Args:
            master_password: The master password.
            salt: The salt for key derivation.
            iterations: The number of iterations for key derivation. Defaults to 100,000.

        Returns:
            The derived key as bytes.
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    @override
    def encrypt(self, plaintext: str, master_password: str) -> str:
        salt = os.urandom(self.SALT_SIZE)
        key = FernetEncryptor.derive_key(master_password, salt)

        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(plaintext.encode())

        return base64.urlsafe_b64encode(salt + encrypted_text).decode()

    @override
    def decrypt(self, ciphertext: str, master_password: str) -> str:
        decoded_data = base64.urlsafe_b64decode(ciphertext.encode())

        salt = decoded_data[: FernetEncryptor.SALT_SIZE]
        encrypted_text = decoded_data[FernetEncryptor.SALT_SIZE :]
        key = FernetEncryptor.derive_key(master_password, salt)

        cipher_suite = Fernet(key)
        try:
            return cipher_suite.decrypt(encrypted_text).decode()
        except InvalidToken as err:
            raise IncorrectMasterPasswordError from err
