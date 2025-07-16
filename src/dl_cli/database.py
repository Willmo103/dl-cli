from sqlalchemy import create_engine
from dl_cli.models import Base
from dl_cli.config import DB_PATH

def _init_db():
    """ Initialize the database connection and create tables if they do not exist. """
    engine = create_engine(f'sqlite:///{DB_PATH}')
    Base.metadata.create_all(engine)
    return engine

if __name__ == '__main__':
    _init_db()
