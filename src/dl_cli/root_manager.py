from dl_cli.models import RootModel, RootFileModel, RootFolderModel

class RootManager:
    """ Manages root directories and their associated files and folders. """

    def __init__(self):
        self.roots = []
        self.load_roots()

    def load_roots(self):
        """ Load root directories from the database. """
        _roots = RootModel.query.all()
