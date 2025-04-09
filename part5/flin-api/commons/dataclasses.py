from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel


class BaseORMDataClass(BaseModel):
    class Config:
        from_attributes = True


class BaseDataClass(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class ErrorResponseMessage(BaseDataClass):
    """
    Represents Error Response Message format
    """

    non_field_errors: List[str]


class JWTDataClass(BaseDataClass):
    access: str
    refresh: str
