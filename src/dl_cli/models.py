from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base: declarative_base = declarative_base()


class RootModel(Base):
    """Represents a root directory in the database."""

    __tablename__ = "roots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    path = Column(String, unique=True, nullable=False)

class RootFileModel(Base):
    """Represents a file in a root directory."""

    __tablename__ = "root_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    root_id = Column(Integer, ForeignKey("roots.id"), nullable=False)
    full_path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)


class RootFolderModel(Base):
    """Represents a folder in a root directory."""

    __tablename__ = "root_folders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    root_id = Column(Integer, ForeignKey("roots.id"), nullable=False)
    full_path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    last_modified = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)


class FolderToProjectTable(Base):
    """Represents the association between folders and projects."""

    __tablename__ = "folder_to_project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    folder_id = Column(Integer, ForeignKey("root_folders.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)


class FilesToProjectTable(Base):
    """Represents the association between files and projects."""

    __tablename__ = "file_to_project"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("root_files.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)


class ProjectModel(Base):
    """Represents a project in the database."""

    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
