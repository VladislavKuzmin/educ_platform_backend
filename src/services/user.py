from typing import Optional

from entities.user import UserEntity
from repositories.user import UserRepository


async def create_user_service(user_entity: UserEntity) -> UserEntity:
    user_repo = await UserRepository.get_repository()
    user_entity.id = (await user_repo.create(user_entity)).inserted_id
    return user_entity


async def get_user_service(identifier: str, identifier_field: str = '_id') -> Optional[UserEntity]:
    user_repo = await UserRepository.get_repository()
    db_user = await user_repo.read(fields={identifier_field: identifier})
    return UserEntity.from_db_model(db_model=db_user) if db_user else None


async def get_users_service() -> list[UserEntity]:
    user_repo = await UserRepository.get_repository()
    users = await user_repo.read_many(fields=None)
    return [UserEntity.from_db_model(db_model=user) for user in users]


async def get_user_subordinates(identifier: str, identifier_field: str = 'boss_id') -> list[UserEntity]:
    user_repo = await UserRepository.get_repository()
    subordinates = await user_repo.read_many(fields={identifier_field: identifier})
    return [UserEntity.from_db_model(db_model=subordinate) for subordinate in subordinates]


async def update_user(user_entity: UserEntity) -> None:
    user_repo = await UserRepository.get_repository()
    await user_repo.update(user_entity)
