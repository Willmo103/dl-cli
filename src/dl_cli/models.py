
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RootModel(Base):
    """ Represents a root directory in the database. """
    __tablename__ = 'roots'
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, unique=True, nullable=False)


class RootFileModel(Base):
    """ Represents a file in a root directory. """
    __tablename__ = 'root_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    root_id = Column(Integer, ForeignKey('roots.id'), nullable=False)
    full_path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)


class RootFolderModel(Base):
    """ Represents a folder in a root directory. """
    __tablename__ = 'root_folders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    root_id = Column(Integer, ForeignKey('roots.id'), nullable=False)
    full_path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)

