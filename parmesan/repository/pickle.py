import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import override

from parmesan.repository.abc import PasswordRepository


@dataclass
class PicklePasswordRepository(PasswordRepository):
    """A password repository that uses [pickle](https://docs.python.org/3/library/pickle.html)
    to store passwords in a file.

    Args:
        path: The path to the pickle file. Defaults to `"passwords.pickle"`.
        passwords: The dictionary to store the passwords. Defaults to an empty dictionary.

    Attributes:
        path: The path to the pickle file.
        passwords: The dictionary to store the passwords.
    """

    path: Path = Path("passwords.pickle")
    passwords: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize the `PicklePasswordRepository`.

        If the pickle file does not exist, an empty dictionary is saved to
        create the file. The passwords are then loaded from the pickle file.
        """

        if not self.path.exists():
            self.save()

        self.passwords = pickle.loads(self.path.read_bytes())  # noqa: S301

    def save(self) -> None:
        """Save the passwords dictionary to the pickle file."""
        self.path.write_bytes(pickle.dumps(self.passwords))

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
