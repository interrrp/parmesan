from abc import ABC, abstractmethod
from typing import override

from cryptography.fernet import Fernet


class Encryptor(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str, master_password: str) -> str: ...
    @abstractmethod
    def decrypt(self, ciphertext: str, master_password: str) -> str: ...


class FernetEncryptor(Encryptor):
    @override
    def encrypt(self, plaintext: str, master_password: str) -> str:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(plaintext.encode()).decode()

    @override
    def decrypt(self, ciphertext: str, master_password: str) -> str:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(ciphertext.encode()).decode()
