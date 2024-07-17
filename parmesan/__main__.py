import typer


def index() -> None:
    print("Hello, world!")


def main() -> None:
    typer.run(index)


if __name__ == "__main__":
    main()
