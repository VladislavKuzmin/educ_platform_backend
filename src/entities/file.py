from typing import Optional

from entities.base import BaseEntity
from repositories.models.file import FileDBModel


class FileEntity(BaseEntity):
    _DB_MODEL = FileDBModel

    id: Optional[str] = None
    extension: Optional[str] = None
