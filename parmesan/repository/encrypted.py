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
        """Get the decrypted password for the given name.

        Args:
            name: The name of the password.

        Returns:
            The decrypted password if found, `None` otherwise.
        """

        encrypted_password = self.base_repository[name]
        if encrypted_password is None:
            return None
        return self.encryptor.decrypt(encrypted_password, self.master_password)

    @override
    def __setitem__(self, name: str, password: str) -> None:
        """Set the encrypted password for the given name.

        Args:
            name: The name of the password.
            password: The password to be encrypted and stored.
        """

        encrypted_password = self.encryptor.encrypt(password, self.master_password)
        self.base_repository[name] = encrypted_password

    @override
    def __delitem__(self, name: str) -> None:
        """Delete the password with the given name.

        Args:
            name: The name of the password.
        """

        if name in self.base_repository:
            del self.base_repository[name]

    @override
    def __contains__(self, name: str) -> bool:
        """Check if the password repository contains a password with the given name.

        Args:
            name: The name of the password.

        Returns:
            `True` if the password exists, `False` otherwise.
        """

        return name in self.base_repository
