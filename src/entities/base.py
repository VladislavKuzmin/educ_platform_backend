from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from repositories.models.base import BaseDBModel
from transport.base_api_schema import BaseApiSchema


class BaseEntity(ABC, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    _DB_MODEL: BaseDBModel

    id: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_db_model(cls, db_model: BaseDBModel):
        return cls.model_validate(db_model.model_dump())

    @classmethod
    def from_api_schema(cls, schema: BaseApiSchema):
        a = schema.model_dump()
        return cls.model_validate(schema.model_dump())

    def to_db_model(self) -> BaseDBModel:
        return self._DB_MODEL.model_validate(self.model_dump(exclude_unset=True))

    def to_api_schema(self, schema: type(BaseApiSchema)):
        return schema.model_validate(self.model_dump())
