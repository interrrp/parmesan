import pyperclip  # pyright: ignore[reportMissingTypeStubs]
from cryptography.fernet import InvalidToken
from rich import print
from rich.prompt import Confirm, Prompt
from typer import Typer

from parmesan import messages
from parmesan.encryption import FernetEncryptor
from parmesan.repository import EncryptedPasswordRepository, PasswordRepository, PicklePasswordRepository

app = Typer()

password_repository: PasswordRepository = EncryptedPasswordRepository(
    PicklePasswordRepository(),
    FernetEncryptor(),
    Prompt.ask("[gray50]Enter master password (hidden)[/gray50]", password=True),
)


@app.command()
@app.command("set")
@app.command("new")
def add(name: str, password: str) -> None:
    if name in password_repository:
        confirm_overwrite = Confirm.ask(messages.CONFIRM_PASSWORD_OVERWRITE)
        if not confirm_overwrite:
            print(messages.ABORTED)
            return

    password_repository[name] = password
    print(messages.SET_PASSWORD.format(length=len(password), name=name))


@app.command()
def get(name: str) -> None:
    if name not in password_repository:
        print(messages.PASSWORD_NOT_FOUND.format(name=name))
        return

    password = password_repository[name]
    pyperclip.copy(password)  # type: ignore[reportUnknownMemberType]
    print(messages.COPY_PASSWORD.format(name=name))


@app.command()
@app.command("delete")
def remove(name: str) -> None:
    if name not in password_repository:
        print(messages.PASSWORD_NOT_FOUND.format(name=name))
        return

    confirm_delete = Confirm.ask(messages.CONFIRM_DELETE.format(name=name))
    if not confirm_delete:
        print(messages.ABORTED)
        return

    # Access the password to see if it can be decrypted. If the wrong master
    # password was entered, it will raise an error and we will not continue.
    password_repository[name]

    del password_repository[name]
    print(messages.REMOVED_PASSWORD.format(name=name))


def main() -> None:
    try:
        app()
    except InvalidToken:
        print("[red]Incorrect master password[/red]")


if __name__ == "__main__":
    main()
