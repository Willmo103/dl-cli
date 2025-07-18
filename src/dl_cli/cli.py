import typer

from dl_cli.root_manager import app


cli = typer.Typer(
    name="utils",
    help="Utility commands for managing the application.",
)


def entrypoint():
    """Main entry point for the CLI."""
    cli()
