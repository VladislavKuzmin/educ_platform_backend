import asyncio
from asyncio import get_event_loop

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from singleton_decorator import singleton

from settings import get_settings


@singleton
class MongoClient:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase

    def __init__(self) -> None:
        if not self.client:
            settings = get_settings()
            self.client = AsyncIOMotorClient(
                settings.mongo.CONNECTION_STRING,
                username=settings.mongo.USER,
                password=settings.mongo.PASS,
                io_loop=asyncio.get_event_loop(),
            )
            self.db = self.client[settings.mongo.DB_NAME]

    def init_client(self) -> None:
        settings = get_settings()
        self.client = AsyncIOMotorClient(
            settings.mongo.CONNECTION_STRING,
            username=settings.mongo.USER,
            password=settings.mongo.PASS,
            io_loop=asyncio.get_event_loop(),
        )
        self.db = self.client[settings.mongo.DB_NAME]

    def close_client(self) -> None:
        if self.client:
            self.client.close()
