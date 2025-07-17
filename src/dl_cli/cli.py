import typer

from dl_cli.root_manager import RootManager

cli = typer.Typer(
    name="utils",
    help="Utility commands for managing the application.",
)


@cli.add_typer(RootManager.app, name="root", help="Manage root directories.")
def entrypoint():
    """Main entry point for the CLI."""
    cli()
