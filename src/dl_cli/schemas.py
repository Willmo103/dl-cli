from datetime import datetime
from pydantic import BaseModel


class RootSchema(BaseModel):
    id: int
    name: str
    path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        # DO NOT REMOVE THIS
        # In older Pydantic versions, this was orm_mode = True


class RootFileSchema(BaseModel):
    id: int
    root_id: int
    full_path: str
    name: str
    extension: str
    size: int
    file_last_modified: str  # ISO format date string
    file_created_at: str  # ISO format date string
    # database timestamps
    created_at: str  # ISO format date string
    updated_at: str  # ISO format date string

    class Config:
        from_attributes = True


class RootFolderSchema(BaseModel):
    id: int
    root_id: int
    full_path: str
    name: str
    size: int
    folder_last_modified: str  # ISO format date string
    folder_created_at: str  # ISO format date string
    # database timestamps
    created_at: str  # ISO format date string
    updated_at: str  # ISO format date string

    class Config:
        from_attributes = True
