from pathlib import Path
from sqlalchemy import Engine
import typer
from dl_cli.models import RootModel
from dl_cli.schemas import RootSchema
from dl_cli.database import db_instance as db


class RootDbManager:
    """Manages root directories and their associated files and folders."""
    _db: Engine | None = db


    @staticmethod
    def create_root(path: str, name: str | None = None) -> RootSchema:
        """Create a new root directory."""
        _path = Path(path)
        if not _path.is_dir():
            raise ValueError(f"The path {_path} is not a valid directory.")
        new_root = RootModel(name=name or _path.name, path=str(_path.resolve()))
        new_root.save()
        return RootSchema(**new_root)

    @staticmethod
    def get_root(name: str | None = None, path: str | None = None) -> "RootSchema":
        """Get a root directory by name or path."""
        if name:
            root = RootModel.query.filter_by(name=name).first()
        elif path:
            root = RootModel.query.filter_by(path=path).first()
        else:
            raise ValueError("Either name or path must be provided.")

        if not root:
            raise ValueError(f"Root with name '{name}' or path '{path}' not found.")

        return RootSchema(**root)

    @staticmethod
    def list_roots() -> list[RootSchema]:
        """List all root directories."""
        roots = RootModel.query.all()
        return [RootSchema(**root) for root in roots]

    @staticmethod
    def delete_root(root_id: int) -> None:
        """Delete a root directory by its ID."""
        root = RootModel.query.get(root_id)
        if not root:
            raise ValueError(f"Root with ID {root_id} not found.")
        root.delete()

    @staticmethod
    def update_root(
        root_id: int, name: str | None = None, path: str | None = None
    ) -> RootSchema:
        """Update an existing root directory."""
        root = RootModel.query.get(root_id)
        if not root:
            raise ValueError(f"Root with ID {root_id} not found.")
        if name:
            root.name = name
        if path:
            new_path = Path(path)
            if not new_path.is_dir():
                raise ValueError(f"The path {new_path} is not a valid directory.")
            root.path = str(new_path.resolve())
        root.save()
        return RootSchema(**root)


class RootManager:
    """CLI for managing root directories."""

    app = typer.Typer(
        name="Root Manager",
        help="Manage root directories and their associated files and folders.",
        no_args_is_help=True
    )

    @app.command(
        help="Create a new root directory."
    )
    def create_root(name: str, path: str):
        """Create a new root directory."""
        root = RootDbManager.create_root(name=name, path=path)
        typer.echo(f"Created root: {root.name} at {root.path}")


    @app.command()
    def get_root(name: str | None = None, path: str | None = None):
        """Get a root directory by name or path."""
        root = RootDbManager.get_root(name=name, path=path)
        typer.echo(f"Found root: {root.name} at {root.path}")

    @app.command()
    def list_roots():
        """List all root directories."""
        roots = RootDbManager.list_roots()
        for root in roots:
            typer.echo(f"Root: {root.name} at {root.path}")

    @app.command()
    def delete_root(root_id: int):
        """Delete a root directory by its ID."""
        RootDbManager.delete_root(root_id=root_id)
        typer.echo(f"Deleted root with ID: {root_id}")

    @app.command()
    def update_root(root_id: int, name: str | None = None, path: str | None = None):
        """Update an existing root directory."""
        root = RootDbManager.update_root(root_id=root_id, name=name, path=path)
        typer.echo(f"Updated root: {root.name} at {root.path}")


if __name__ == "__main__":
    RootManager.app()
