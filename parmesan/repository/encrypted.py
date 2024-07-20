from dataclasses import dataclass
from typing import override

from parmesan.encryption import Encryptor
from parmesan.repository.abc import PasswordRepository


@dataclass
class EncryptedPasswordRepository(PasswordRepository):
    """A password repository that encrypts and decrypts passwords using an encryptor and a master password.

    Args:
        base_repository: The base password repository.
        encryptor: The encryptor used for encryption and decryption.
        master_password: The master password used for encryption and decryption.

    Attributes:
        base_repository The base password repository.
        encryptor: The encryptor used for encryption and decryption.
        master_password: The master password used for encryption and decryption.
    """

    base_repository: PasswordRepository
    encryptor: Encryptor
    master_password: str

    @override
    def __getitem__(self, name: str) -> str | None:
        encrypted_password = self.base_repository[name]
        if encrypted_password is None:
            return None
        return self.encryptor.decrypt(encrypted_password, self.master_password)

    @override
    def __setitem__(self, name: str, password: str) -> None:
        encrypted_password = self.encryptor.encrypt(password, self.master_password)
        self.base_repository[name] = encrypted_password

    @override
    def __delitem__(self, name: str) -> None:
        if name in self.base_repository:
            del self.base_repository[name]

    @override
    def __contains__(self, name: str) -> bool:
        return name in self.base_repository
