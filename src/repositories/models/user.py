from typing import Optional

from pydantic import EmailStr

from repositories.models.base import BaseDBModel


class UserDBModel(BaseDBModel):
    email: EmailStr
    is_admin: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None
    boss_id: Optional[str] = None
