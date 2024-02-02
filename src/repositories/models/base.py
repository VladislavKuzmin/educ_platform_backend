from abc import ABC
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


class BaseDBModel(ABC, BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: str = Field(alias="_id", default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default=datetime.utcnow())
