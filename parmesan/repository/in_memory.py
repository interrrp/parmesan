from dataclasses import dataclass, field
from typing import override

from parmesan.repository.abc import PasswordRepository


@dataclass
class InMemoryPasswordRepository(PasswordRepository):
    """In-memory implementation of a password repository.

    This class stores passwords in memory using a dictionary.

    Attributes:
        passwords: A dictionary that maps names to passwords.
    """

    passwords: dict[str, str] = field(default_factory=dict)

    @override
    def __getitem__(self, name: str) -> str | None:
        return self.passwords.get(name)

    @override
    def __setitem__(self, name: str, password: str) -> None:
        self.passwords[name] = password

    @override
    def __delitem__(self, name: str) -> None:
        del self.passwords[name]

    @override
    def __contains__(self, name: str) -> bool:
        return name in self.passwords
