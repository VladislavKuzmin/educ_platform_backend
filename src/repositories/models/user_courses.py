from typing import Optional
from pydantic import Field

from repositories.models.base import BaseDBModel


class UserCourseDBModel(BaseDBModel):
    user_id: str
    course_id: str
    completed_subchapters: list[int] = Field(default_factory=list)
    last_viewed_subchapter: int = 0
    is_completed: bool = False
    is_archived: bool = False
    assigned_by: Optional[str] = None
