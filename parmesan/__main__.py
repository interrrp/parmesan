import pyperclip  # pyright: ignore[reportMissingTypeStubs]
from rich import print
from rich.prompt import Confirm
from typer import Typer

from parmesan.repository import PasswordRepository, PicklePasswordRepository

app = Typer()
password_repository: PasswordRepository = PicklePasswordRepository()


@app.command()
@app.command("set")
@app.command("new")
def add(name: str, password: str) -> None:
    if name in password_repository:
        confirm_overwrite = Confirm.ask(
            "[orange1]A password with this name already exists. Overwrite?[/orange1]",
        )
        if not confirm_overwrite:
            print("[red]Aborted.[/red]")
            return

    password_repository[name] = password
    print(f"[green]Set {len(password)}-character password for [bold]{name}[/bold].[/green]")


@app.command()
def get(name: str) -> None:
    if name not in password_repository:
        print(f"[red]A password with the name [bold]{name}[/bold] doesn't exist.[/red]")
        return

    password = password_repository[name]
    pyperclip.copy(password)  # pyright: ignore[reportUnknownMemberType]
    print(f"[green]📋 Copied [bold]{name}[/bold] password to clipboard.[/green]")


@app.command()
@app.command("delete")
def remove(name: str) -> None:
    if name not in password_repository:
        print(f"[red]A password with the name [bold]{name}[/bold] doesn't exist.[/red]")
        return

    confirm_delete = Confirm.ask(
        f"[orange1]Are you sure you want to delete the password for [bold]{name}[/bold]?[/orange1]",
    )
    if not confirm_delete:
        print("[red]Aborted.[/red]")
        return

    del password_repository[name]
    print(f"[green]Removed password for [bold]{name}[/bold].[/green]")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
