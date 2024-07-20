from abc import ABC, abstractmethod


class Encryptor(ABC):
    """Abstract base class for encryption and decryption operations."""

    @abstractmethod
    def encrypt(self, plaintext: str, master_password: str) -> str:
        """Encrypt the given plaintext using the master password.

        Args:
            plaintext: The text to encrypt.
            master_password: The master password used for encryption.

        Returns:
            The encrypted text as a string.
        """

    @abstractmethod
    def decrypt(self, ciphertext: str, master_password: str) -> str:
        """Encrypt the given plaintext using the master password.

        Args:
            plaintext: The text to encrypt.
            master_password: The master password used for encryption.

        Returns:
            The encrypted text as a string.
        """
