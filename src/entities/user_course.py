from typing import Optional

from pydantic import Field

from entities.base import BaseEntity
from repositories.models.user_courses import UserCourseDBModel


class UserCourseEntity(BaseEntity):
    _DB_MODEL = UserCourseDBModel

    user_id: Optional[str] = None
    course_id: Optional[str] = None
    completed_subchapters: Optional[list[int]] = Field(default_factory=list)
    last_viewed_subchapter: Optional[int] = 0
    is_completed: Optional[bool] = None
    is_archived: Optional[bool] = None
    assigned_by: Optional[str] = None
