import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import override

from parmesan.encryption import Encryptor


class PasswordRepository(ABC):
    @abstractmethod
    def __getitem__(self, name: str) -> str | None: ...
    @abstractmethod
    def __setitem__(self, name: str, password: str) -> None: ...
    @abstractmethod
    def __delitem__(self, name: str) -> None: ...
    @abstractmethod
    def __contains__(self, name: str) -> bool: ...


@dataclass
class PicklePasswordRepository(PasswordRepository):
    path: Path = Path("passwords.pickle")
    passwords: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.path.exists():
            # The passwords dict is empty at this point, so we save it to create the Pickle file
            self.save()

        self.passwords = pickle.loads(self.path.read_bytes())  # noqa: S301

    def save(self) -> None:
        _ = self.path.write_bytes(pickle.dumps(self.passwords))

    @override
    def __getitem__(self, name: str) -> str | None:
        return self.passwords.get(name)

    @override
    def __setitem__(self, name: str, password: str) -> None:
        self.passwords[name] = password
        self.save()

    @override
    def __delitem__(self, name: str) -> None:
        del self.passwords[name]
        self.save()

    @override
    def __contains__(self, name: str) -> bool:
        return name in self.passwords


@dataclass
class EncryptedPasswordRepository(PasswordRepository):
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
