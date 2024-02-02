from repositories.base import MongoDBRepositoryBase
from repositories.models.file import FileDBModel


class FileRepository(
    MongoDBRepositoryBase,
):
    _COLLECTION_NAME = 'file'
    _COLLECTION_MODEL = FileDBModel
