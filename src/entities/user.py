from typing import Optional

from pydantic import EmailStr

from entities.base import BaseEntity
from repositories.models.user import UserDBModel
from services.data_types import GoogleToken


class UserEntity(BaseEntity):
    _DB_MODEL = UserDBModel

    id: Optional[str] = None
    is_admin: Optional[bool] = False
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None
    boss_id: Optional[str] = None

    @classmethod
    def from_google_oauth_token(cls, token: GoogleToken) -> 'UserEntity':
        return cls(
            email=token.userinfo.email,
            first_name=token.userinfo.given_name,
            last_name=token.userinfo.family_name,
            image_url=token.userinfo.picture,
            is_admin=False,
            boss_id=None
        )
