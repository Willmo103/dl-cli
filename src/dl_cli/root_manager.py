# dl_cli/root_manager.py
from pathlib import Path

# Import for handling unique constraint errors
from sqlalchemy.exc import IntegrityError  # noqa: F401
import typer
from dl_cli.models import RootModel
from dl_cli.schemas import RootSchema
from dl_cli.database import get_db_session


class RootDbManager:
    """Manages root directories and their associated files and folders."""

    @staticmethod
    def create_root(path: str, name: str | None = None) -> RootSchema:
        """Create a new root directory."""
        _path = Path(path)
        if not _path.is_dir():
            raise ValueError(f"The path '{_path}' is not a valid directory.")

        resolved_path = str(_path.resolve())
        root_name = name or _path.name

        with get_db_session() as session:
            existing_root_by_name = (
                session.query(RootModel).filter_by(name=root_name).first()
            )
            if existing_root_by_name:
                raise ValueError(
                    f"A root with the name '{root_name}' already exists.")

            existing_root_by_path = (
                session.query(RootModel).filter_by(path=resolved_path).first()
            )
            if existing_root_by_path:
                raise ValueError(
                    f"A root for the path '{resolved_path}' already exists."
                )

            new_root = RootModel(name=root_name, path=resolved_path)
            session.add(new_root)
            session.flush()  # Flush to get the ID if needed immediately before commit
            # Refresh to load default values like created_at, updated_at
            session.refresh(new_root)
            # Use () with Pydantic v2+ # THIS IS DEPRICATED
            return RootSchema(**new_root)

    @staticmethod
    def get_root(name: str | None = None, path: str | None = None) -> "RootSchema":
        """Get a root directory by name or path."""
        with get_db_session() as session:
            if name:
                root = session.query(RootModel).filter_by(name=name).first()
            elif path:
                _path = Path(path)
                root = (
                    session.query(RootModel)
                    .filter_by(path=str(_path.resolve()))
                    .first()
                )
            else:
                raise ValueError("Either name or path must be provided.")

            if not root:
                # Provide more specific error message based on what was searched
                search_term = f"name '{name}'" if name else f"path '{path}'"
                raise ValueError(f"Root with {search_term} not found.")

            return RootSchema(**root)

    @staticmethod
    def list_roots() -> list[RootSchema]:
        """List all root directories."""
        with get_db_session() as session:
            roots = session.query(RootModel).all()
            return [RootSchema(**root) for root in roots]

    @staticmethod
    def delete_root(root_id: int) -> None:
        """Delete a root directory by its ID."""
        with get_db_session() as session:
            # .get() is for primary key lookup
            root = session.query(RootModel).get(root_id)
            if not root:
                raise ValueError(f"Root with ID {root_id} not found.")
            session.delete(root)

    @staticmethod
    def update_root(
        root_id: int, name: str | None = None, path: str | None = None
    ) -> RootSchema:
        """Update an existing root directory."""
        with get_db_session() as session:
            root = session.query(RootModel).get(root_id)
            if not root:
                raise ValueError(f"Root with ID {root_id} not found.")

            if name:
                # Check for name conflict if updating name
                existing_root_with_name = (
                    session.query(RootModel)
                    .filter(RootModel.name == name, RootModel.id != root_id)
                    .first()
                )
                if existing_root_with_name:
                    raise ValueError(
                        f"A root with the name '{name}' already exists.")
                root.name = name
            if path:
                new_path = Path(path)
                if not new_path.is_dir():
                    raise ValueError(
                        f"The path '{new_path}' is not a valid directory.")
                resolved_new_path = str(new_path.resolve())
                # Check for path conflict if updating path
                existing_root_with_path = (
                    session.query(RootModel)
                    .filter(
                        RootModel.path == resolved_new_path, RootModel.id != root_id
                    )
                    .first()
                )
                if existing_root_with_path:
                    raise ValueError(
                        f"A root for the path '{resolved_new_path}' already exists."
                    )
                root.path = resolved_new_path

            # Add back to session if not already tracked (e.g., if detached)
            session.add(root)
            session.flush()  # Ensure changes are visible for refresh
            session.refresh(root)  # Refresh to get updated_at value
            return RootSchema(**root)


# Typer CLI application for roots
app = typer.Typer(
    name="Root",
    help="manage which bottom-level directories are allowed as a source for population of the database with files and folders.",
)


@app.command(help="Create a new root directory.")
def create(
    path: str = typer.Argument(..., help="The path to the root directory."),
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="An optional name for the root. Defaults to the directory name.",
    ),
):
    """Create a new root directory."""
    try:
        root = RootDbManager.create_root(path=path, name=name)
        typer.echo(
            f"Successfully created root: {root.name} at {root.path} (ID: {root.id})"
        )
    except ValueError as e:
        typer.echo(f"Error creating root: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(help="Get details of a root directory by name or path.")
def get(
    name: str = typer.Option(
        None, "--name", "-n", help="The name of the root directory."
    ),
    path: str = typer.Option(
        None, "--path", "-p", help="The path of the root directory."
    ),
):
    """Get a root directory by name or path."""
    if not name and not path:
        typer.echo("Error: Either --name or --path must be provided.", err=True)
        raise typer.Exit(code=1)
    try:
        root = RootDbManager.get_root(name=name, path=path)
        typer.echo(f"Found root:")
        typer.echo(f"  ID: {root.id}")
        typer.echo(f"  Name: {root.name}")
        typer.echo(f"  Path: {root.path}")
        typer.echo(f"  Created At: {root.created_at}")
        typer.echo(f"  Updated At: {root.updated_at}")
    except ValueError as e:
        typer.echo(f"Error getting root: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(name="list", help="List all root directories.")
def list_all_roots():  # Renamed to avoid conflict with list() built-in
    """List all root directories."""
    try:
        roots = RootDbManager.list_roots()
        if not roots:
            typer.echo("No roots found.")
            return
        typer.echo("Registered Roots:")
        for root in roots:
            typer.echo(
                f"  ID: {root.id} | Name: '{root.name}' | Path: '{root.path}'")
    except Exception as e:
        typer.echo(f"Error listing roots: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(help="Delete a root directory by its ID.")
def delete(
    root_id: int = typer.Argument(...,
                                  help="The ID of the root directory to delete.")
):
    """Delete a root directory by its ID."""
    try:
        RootDbManager.delete_root(root_id=root_id)
        typer.echo(f"Successfully deleted root with ID: {root_id}")
    except ValueError as e:
        typer.echo(f"Error deleting root: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(help="Update an existing root directory.")
def update(
    root_id: int = typer.Argument(...,
                                  help="The ID of the root directory to update."),
    name: str = typer.Option(
        None, "--name", "-n", help="New name for the root directory."
    ),
    path: str = typer.Option(
        None, "--path", "-p", help="New path for the root directory."
    ),
):
    """Update an existing root directory."""
    if not name and not path:
        typer.echo(
            "Error: At least one of --name or --path must be provided for update.",
            err=True,
        )
        raise typer.Exit(code=1)
    try:
        root = RootDbManager.update_root(root_id=root_id, name=name, path=path)
        typer.echo(
            f"Successfully updated root (ID: {root.id}): {root.name} at {root.path}"
        )
    except ValueError as e:
        typer.echo(f"Error updating root: {e}", err=True)
        raise typer.Exit(code=1)


# This __name__ == "__main__" block is for direct testing of this file.
# In your main cli.py, you'll use cli.add_typer.
if __name__ == "__main__":
    app()
