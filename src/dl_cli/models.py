import datetime
from typing import Any
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base: Any = declarative_base()


class RootModel(Base):
    """Represents a root directory in the database."""

    __tablename__ = "roots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Added unique=True for name consistency
    name = Column(String, nullable=False, unique=True)
    path = Column(String, unique=True, nullable=False)
    # Auto-set creation time
    created_at = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )

    def __repr__(self):
        return f"<Root(id={self.id}, name='{self.name}', path='{self.path}')>"


class RootFileModel(Base):
    """Represents a file in a root directory."""

    __tablename__ = "root_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    root_id = Column(Integer, ForeignKey("roots.id"), nullable=False)
    full_path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    file_last_modified = Column(DateTime, nullable=False)
    file_created_at = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )


class RootFolderModel(Base):
    """Represents a folder in a root directory."""

    __tablename__ = "root_folders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    root_id = Column(Integer, ForeignKey("roots.id"), nullable=False)
    full_path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    folder_last_modified = Column(DateTime, nullable=False)
    folder_created_at = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )


__all__ = [
    "RootModel",
    "RootFileModel",
    "RootFolderModel",
]
