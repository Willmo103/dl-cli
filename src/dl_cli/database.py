from sqlalchemy import create_engine
from .models import Base, RootModel, RootFileModel, RootFolderModel
from .config import DB_PATH

def _init_db():
    """ Initialize the database connection and create tables if they do not exist. """
    engine = create_engine(f'sqlite:///{DB_PATH}')
    Base.metadata.create_all(engine)
    return engine

