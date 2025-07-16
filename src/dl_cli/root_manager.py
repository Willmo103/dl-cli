from pathlib import Path
from typing import List
from dl_cli.models import RootModel, RootFileModel, RootFolderModel
from dl_cli.schemas import RootSchema, RootFileSchema, RootFolderSchema


class RootDbManager:
    """ Manages root directories and their associated files and folders. """

    @staticmethod
    def create_root(path: str, name: str | None = None) -> RootSchema:
        """ Create a new root directory. """
        path = Path(path)
        if not path.is_dir():
            raise ValueError(f"The path {path} is not a valid directory.")
        new_root = RootModel(name=name or path.name, path=str(path.resolve()))
        new_root.save()
        return RootSchema(**new_root)

    @staticmethod
    def get_root(name: str | None = None, path: str | None = None) -> RootSchema:
        """ Get a root directory by name or path. """
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
        """ List all root directories. """
        roots = RootModel.query.all()
        return [RootSchema(**root) for root in roots]

    @staticmethod
    def delete_root(root_id: int) -> None:
        """ Delete a root directory by its ID. """
        root = RootModel.query.get(root_id)
        if not root:
            raise ValueError(f"Root with ID {root_id} not found.")
        root.delete()

    @staticmethod
    def update_root(root_id: int, name: str | None = None, path: str | None = None) -> RootSchema:
        """ Update an existing root directory. """
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


class RootScanner:
    """ Manages files within root directories. """
    _root_id: int
    _roots: List[RootModel] = []

    def __init__(self, root_id: int):
        """ Initialize the scanner with a root ID. """
        self._root_id = root_id
        self._root = RootModel.query.get(root_id)
        if not self._root:
            raise ValueError(f"Root with ID {root_id} not found.")
