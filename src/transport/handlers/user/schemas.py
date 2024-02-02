from typing import Optional

from pydantic import EmailStr

from transport.base_api_schema import BaseApiSchema


class GetUserRequestSchema(BaseApiSchema):
    id: str


class GetUserSubordinatesRequestSchema(BaseApiSchema):
    user_id: str


class GetUserResponseSchema(BaseApiSchema):
    id: str
    email: EmailStr
    is_admin: bool
    first_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    boss_id: Optional[str]


class GetUsersResponseSchema(BaseApiSchema):
    items: list[GetUserResponseSchema]


class UpdateUserRequestSchema(BaseApiSchema):
    id: str
    boss_id: Optional[str]
