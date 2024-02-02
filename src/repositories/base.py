from abc import ABC
from typing import Optional, Any

from async_lru import alru_cache
from bson import CodecOptions
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession, AsyncIOMotorCollection
from pymongo.results import InsertOneResult

from entities.base import BaseEntity
from integrations.mongodb.client import MongoClient
from repositories.models.base import BaseDBModel


class MongoDBRepositoryBase(ABC):
    _COLLECTION_NAME: str
    _COLLECTION_MODEL: type[BaseDBModel]
    _REGULAR_INDEXES: tuple[str, ...] = ()
    _UNIQUE_INDEXES: tuple[str, ...] = ()

    def __init__(
            self,
            db: AsyncIOMotorDatabase,
            *,
            session: AsyncIOMotorClientSession | None = None,
    ) -> None:
        self._session: AsyncIOMotorClientSession | None = session
        self._db: AsyncIOMotorDatabase = db
        self._collection: AsyncIOMotorCollection = db[self._COLLECTION_NAME]
        self._collection = self._collection.with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=None))

    async def create_indexes(
            self,
    ) -> None:
        for index_name in self._REGULAR_INDEXES:
            await self._collection.create_index(index_name)
        for index_name in self._UNIQUE_INDEXES:
            await self._collection.create_index(index_name, unique=True)

    async def create(
            self,
            obj: BaseEntity,
    ) -> InsertOneResult:
        return await self._collection.insert_one(obj.to_db_model().model_dump(by_alias=True), session=self._session)

    async def create_many(
            self,
            objs: list[BaseEntity],
    ) -> None:
        await self._collection.insert_many([obj.to_db_model().model_dump(by_alias=True) for obj in objs],
                                           session=self._session)

    async def read_by_id(
            self,
            obj_id: str,
    ):
        data = await self._collection.find_one({"_id": obj_id}, session=self._session)
        return self._COLLECTION_MODEL.model_validate(data) if data else None

    async def read(
            self,
            fields: dict[str, Any],
    ):
        data = await self._collection.find_one(fields, session=self._session)
        return self._COLLECTION_MODEL.model_validate(data) if data else None

    async def delete(
            self,
            obj_id: str,
    ) -> None:
        await self._collection.delete_many({'_id': obj_id}, session=self._session)

    async def read_many(
            self,
            fields: Optional[dict],
            limit: int = 0,
            offset: int = 0,
    ) -> list[BaseDBModel]:
        if not fields:
            fields = {}
        items = self._collection.find(fields).skip(offset).limit(limit)
        return [self._COLLECTION_MODEL.model_validate(item) async for item in items]

    async def read_many_with_specific_fields(
            self,
            fields_to_include: list[str],
            fields: Optional[dict] = None,
    ) -> list[dict]:
        if not fields:
            fields = {}
        items = self._collection.find(fields, {field: 1 for field in fields_to_include})
        formatted_items = []
        async for item in items:
            item['id'] = item.pop('_id')
            formatted_items.append(item)
        return formatted_items

    async def replace(
            self,
            obj: BaseEntity,
    ) -> None:
        await self._collection.replace_one({'_id': obj.id}, obj.to_db_model().model_dump(by_alias=True),
                                           session=self._session)

    @classmethod
    @alru_cache
    async def get_repository(cls, session: Optional[AsyncIOMotorClientSession] = None):
        return cls(db=MongoClient().db, session=session)
