from fastapi import Request

from entities.user import UserEntity
from exceptions.auth import GoogleOAuthError


async def get_current_user(request: Request) -> UserEntity:
    user = request.session.get('user')

    if user is None:
        raise GoogleOAuthError()

    return UserEntity.model_validate(user)
