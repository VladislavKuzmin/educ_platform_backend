from repositories.base import MongoDBRepositoryBase
from repositories.models.user import UserDBModel
from entities.user import UserEntity


class UserRepository(
    MongoDBRepositoryBase,
):
    _COLLECTION_NAME = 'user'
    _COLLECTION_MODEL = UserDBModel

    async def update(
            self,
            obj: UserEntity,
    ) -> None:
        await self._collection.update_one(
            {
                '_id': obj.id
            },
            {
                '$set': obj.model_dump(exclude_unset=True, exclude_defaults=True)
            },
        )
        