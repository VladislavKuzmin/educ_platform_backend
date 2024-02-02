from typing import Optional

from pydantic import Field

from transport.base_api_schema import BaseApiSchema


class GetUserCourseProgressionRequestSchema(BaseApiSchema):
    course_id: str
    user_id: str


class GetUserCourseProgressionResponseSchema(BaseApiSchema):
    user_id: str
    course_id: str
    completed_subchapters: list[int]
    last_viewed_subchapter: int
    is_completed: bool
    is_archived: bool
    assigned_by: Optional[str]


class GetUserCoursesRequestSchema(BaseApiSchema):
    user_id: str


class GetAssignedCourseProgressionsRequestSchema(BaseApiSchema):
    course_id: str
    assigned_by: str

    
class GetUserCoursesResponseSchema(BaseApiSchema):
    items: list[GetUserCourseProgressionResponseSchema]


class PostUserCourseRequestSchema(BaseApiSchema):
    course_id: str
    user_id: str
    assigned_by: Optional[str] = None


class UpdateUserCourseRequestSchema(BaseApiSchema):
    user_id: str
    course_id: str
    completed_subchapters: list[int] = Field(default_factory=list)
    last_viewed_subchapter: int = 0
    is_completed: Optional[bool] = None
    is_archived: Optional[bool] = None


class SubmitTestRequestSchema(BaseApiSchema):
    course_id: str
    subchapter_id: int
    answers: list[list[int]]


class SubmitTestResponseSchema(BaseApiSchema):
    answered_correctly: list[int]
