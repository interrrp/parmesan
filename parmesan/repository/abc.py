from abc import ABC, abstractmethod


class PasswordRepository(ABC):
    """Abstract base class for a password repository.

    This class defines the interface for a password repository, which is
    responsible for storing and retrieving passwords.

    Subclasses of `PasswordRepository` must implement the abstract methods
    defined in this class.

    Attributes:
        __getitem__: Get a password.
        __setitem__: Set a password.
        __delitem__: Delete a password.
        __contains__: Check if a password exists.
    """

    @abstractmethod
    def __getitem__(self, name: str) -> str | None:
        """Get a password.

        For example, you may do `repository["Google"]` to access the password
        with the name `Google`.

        Args:
            name: The name of the password.

        Returns:
            The password, or `None` if a password with the given name doesn't exist.
        """

    @abstractmethod
    def __setitem__(self, name: str, password: str) -> None:
        """Set a password.

        For example, you may do `repository["Google"] = "secretpassword123"` to
        set the password named `Google` to `secretpassword123`.

        Args:
            name: The name of the password.
            password: The password.
        """

    @abstractmethod
    def __delitem__(self, name: str) -> None:
        """Delete a password.

        For example, you may do `del repository["Google"]` to delete the password
        with the name `Google`.

        Args:
            name: The name of the password.
        """

    @abstractmethod
    def __contains__(self, name: str) -> bool:
        """Check if a password exists.

        For example, you may do `if "Google" in repository:` to check if a
        password with the name `Google` exists.

        Args:
            name: The name of the password.

        Returns:
            True if a password with the given name exists, False otherwise.
        """
