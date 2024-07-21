import sqlite3
from dataclasses import dataclass, field
from typing import override

from parmesan.repository.abc import PasswordRepository


@dataclass
class SqlitePasswordRepository(PasswordRepository):
    """SQLite implementation of a password repository.

    This class stores passwords in a SQLite database.

    Attributes:
        db_path: The path to the SQLite database file. Defaults to `"passwords.db"`.
        connection: The SQLite database connection.
    """

    db_path: str = "passwords.db"
    connection: sqlite3.Connection = field(init=False)

    def __post_init__(self) -> None:
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                name TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)

    @override
    def __getitem__(self, name: str) -> str | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT password FROM passwords WHERE name = ?", (name,))
        result: str | None = cursor.fetchone()
        return result[0] if result else None

    @override
    def __setitem__(self, name: str, password: str) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO passwords (name, password) VALUES (?, ?)",
            (name, password),
        )
        self.connection.commit()

    @override
    def __delitem__(self, name: str) -> None:
        self.connection.execute("DELETE FROM passwords WHERE name = ?", (name,))
        self.connection.commit()

    @override
    def __contains__(self, name: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM passwords WHERE name = ?", (name,))
        return cursor.fetchone() is not None

    def __del__(self) -> None:
        if hasattr(self, "connection"):
            self.connection.close()
