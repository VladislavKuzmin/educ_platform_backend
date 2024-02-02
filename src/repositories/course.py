from typing import Any, Optional

from entities.course import CourseEntity
from repositories.base import MongoDBRepositoryBase
from repositories.models.course import CourseDBModel


class CourseRepository(
    MongoDBRepositoryBase,
):
    _COLLECTION_NAME = 'course'
    _COLLECTION_MODEL = CourseDBModel

    async def read_courses_cards(self, fields: Optional[dict[str, Any]]) -> list[CourseEntity]:
        course_repo = await CourseRepository.get_repository()
        fields_to_include = ['_id', 'title', 'description', 'tags', 'estimation', 'total_subchapters']
        courses = await course_repo.read_many_with_specific_fields(
            fields_to_include=fields_to_include,
            fields=fields
        )
        return [CourseEntity.model_validate(course) for course in courses]
