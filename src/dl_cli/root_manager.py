from dl_cli.models import RootModel, RootFileModel, RootFolderModel
from dl_cli.schemas import RootSchema, RootFileSchema, RootFolderSchema

class RootDbManager:
    """ Manages root directories and their associated files and folders. """

    @staticmethod
    def create_root(name: str, path: str) -> RootSchema:
        """ Create a new root directory. """
        new_root = RootModel(name=name, path=path)
        new_root.save()
        return RootSchema(**new_root)

    @staticmethod
    def get_root_by_id(root_id: int) -> RootSchema:
        """ Retrieve a root directory by its ID. """
        root = RootModel.query.get(root_id)
        if not root:
            raise ValueError(f"Root with ID {root_id} not found.")
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
