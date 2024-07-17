from typer import Typer

app = Typer()


@app.command()
@app.command("set")
@app.command("new")
def add(name: str, password: str) -> None:
    print(f"Added {len(password)}-character password for {name}")


@app.command()
@app.command("delete")
def remove(name: str) -> None:
    print(f"Removed password for {name}")


@app.command()
@app.command("set-master")
def set_master_password(password: str) -> None:
    print("Re-encrypting passwords")
    print(f"Set {len(password)}-character master password")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
