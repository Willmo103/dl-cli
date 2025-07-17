from pydantic import BaseModel, Field


class RootSchema(BaseModel):
    name: str
    path: str

    class Config:
        from_attributes = True


class RootFileSchema(BaseModel):
    id: int
    root_id: int
    full_path: str
    name: str
    extension: str
    size: int
    last_modified: str  # ISO format date string
    created_at: str  # ISO format date string

    class Config:
        from_attributes = True


class RootFolderSchema(BaseModel):
    id: int
    root_id: int
    full_path: str
    name: str
    size: int
    last_modified: str  # ISO format date string
    created_at: str  # ISO format date string

    class Config:
        from_attributes = True
