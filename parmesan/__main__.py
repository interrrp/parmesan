import pyperclip  # pyright: ignore[reportMissingTypeStubs]
from rich import print
from rich.prompt import Confirm
from typer import Typer

from parmesan import messages
from parmesan.repository import PasswordRepository, PicklePasswordRepository

app = Typer()
password_repository: PasswordRepository = PicklePasswordRepository()


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
    print(messages.SET_PASSWORD.format(len(password), name))


@app.command()
def get(name: str) -> None:
    if name not in password_repository:
        print(messages.PASSWORD_NOT_FOUND.format(name))
        return

    password = password_repository[name]
    pyperclip.copy(password)  # pyright: ignore[reportUnknownMemberType]
    print(messages.COPY_PASSWORD.format(name))


@app.command()
@app.command("delete")
def remove(name: str) -> None:
    if name not in password_repository:
        print(messages.PASSWORD_NOT_FOUND.format(name))
        return

    confirm_delete = Confirm.ask(messages.CONFIRM_DELETE.format(name))
    if not confirm_delete:
        print(messages.ABORTED)
        return

    del password_repository[name]
    print(messages.REMOVED_PASSWORD.format(name))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
