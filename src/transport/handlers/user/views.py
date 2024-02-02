from fastapi import Depends

from exceptions.user import UserNotFound
from services.user import get_user_service, get_user_subordinates, get_users_service, update_user
from entities.user import UserEntity
from transport.handlers.user.schemas import GetUserResponseSchema, GetUserSubordinatesRequestSchema, GetUsersResponseSchema, GetUserRequestSchema, UpdateUserRequestSchema
from transport.routers import client_router


@client_router.get(
    path='/user',
    summary='Получение пользователя',
    response_model=GetUserResponseSchema,
    response_model_by_alias=True,
)
async def get_user_view(
        request: GetUserRequestSchema = Depends(),
) -> GetUserResponseSchema:
    if not (user_entity := await get_user_service(identifier=request.id)):
        raise UserNotFound()
    return user_entity.to_api_schema(GetUserResponseSchema)


@client_router.get(
    path='/users',
    summary='Получение всех пользователей',
    response_model=GetUsersResponseSchema,
    response_model_by_alias=True,
)
async def get_users_view() -> GetUsersResponseSchema:
    users = await get_users_service()
    return GetUsersResponseSchema(
        items=[user.to_api_schema(GetUserResponseSchema) for user in users]
    )


@client_router.get(
    path='/user/subordinates',
    summary='Получение подчиненных пользователя',
    response_model=GetUsersResponseSchema,
    response_model_by_alias=True,
)
async def get_user_subordinates_view(
    request: GetUserSubordinatesRequestSchema = Depends(),
) -> GetUsersResponseSchema:
    users = await get_user_subordinates(identifier=request.user_id)
    return GetUsersResponseSchema(
        items=[user.to_api_schema(GetUserResponseSchema) for user in users]
    )


@client_router.patch(
    path='/user',
    summary='Обновление пользователя',
    status_code=204
)
async def update_user_view(
    request: UpdateUserRequestSchema,
):
    user_entity = UserEntity.from_api_schema(schema=request)
    await update_user(user_entity=user_entity)
