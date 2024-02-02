from typing import Optional

from constants import ContentType
from entities.course import CourseEntity
from repositories.course import CourseRepository


async def create_course_service(course_entity: CourseEntity) -> None:
    course_repo = await CourseRepository.get_repository()
    for chapter in course_entity.chapters:
        course_entity.total_subchapters += len(chapter.sub_chapters)

    await course_repo.create(course_entity)


async def get_course_service(course_id: str) -> CourseEntity:
    course_repo = await CourseRepository.get_repository()
    course_entity = CourseEntity.from_db_model(await course_repo.read_by_id(obj_id=course_id))

    for chapter in course_entity.chapters:
        for subchapter in chapter.sub_chapters:
            if subchapter.content.type is ContentType.TEST:
                for question in subchapter.content.data.questions:
                    question.answers = []
    return course_entity


async def get_courses_cards_service(courses_ids: Optional[str]) -> list[CourseEntity]:
    course_repo = await CourseRepository.get_repository()
    fields = {'_id': {'$in': courses_ids.split(',')}} if courses_ids else None
    courses = await course_repo.read_courses_cards(fields=fields)
    return [CourseEntity.from_db_model(course) for course in courses]


async def get_course_demo_service() -> list[CourseEntity]:
    course_repo = await CourseRepository.get_repository()
    courses = await course_repo.read_courses_cards()
    return [CourseEntity.from_db_model(course) for course in courses]
