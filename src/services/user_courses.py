from typing import Optional

from entities.user_course import UserCourseEntity
from repositories.user_course import UserCourseRepository


async def get_user_courses_service(user_id: str) -> list[UserCourseEntity]:
    user_course_repo = await UserCourseRepository.get_repository()
    db_user_courses = await user_course_repo.read_many(
        fields={
            'user_id': user_id,
        }
    )
    return [UserCourseEntity.from_db_model(course) for course in db_user_courses]


async def get_user_progression_service(user_id: str, course_id: str) -> Optional[UserCourseEntity]:
    user_course_repo = await UserCourseRepository.get_repository()
    db_user_course = await user_course_repo.read(
        fields={
            'user_id': user_id,
            'course_id': course_id,
            'is_archived': False
        }
    )
    return UserCourseEntity.from_db_model(db_user_course) if db_user_course else None


async def get_assigned_course_progressions_service(course_id: str, assigned_by: str) -> list[UserCourseEntity]:
    user_course_repo = await UserCourseRepository.get_repository()
    db_user_courses = await user_course_repo.read_many(
        fields={
            'course_id': course_id,
            'assigned_by': assigned_by
        }
    )
    return [UserCourseEntity.from_db_model(course) for course in db_user_courses]


async def sign_up_for_course_service(
        user_id: str,
        course_id: str,
        assigned_by: Optional[str]
) -> None:
    user_course_repo = await UserCourseRepository.get_repository()

    archived_user_course = await user_course_repo.read(
        fields={
            'user_id': user_id,
            'course_id': course_id,
            'is_archived': True
        }
    )

    if archived_user_course:
        await user_course_repo.update_with_push(
            UserCourseEntity(
                user_id=user_id,
                course_id=course_id,
                is_archived=False
            )
        )
    else:
        await user_course_repo.create(
            obj=UserCourseEntity(
                user_id=user_id,
                course_id=course_id,
                assigned_by=assigned_by
            )
        )


async def sign_out_from_course_service(user_id: str, course_id: str) -> None:
    user_course_repo = await UserCourseRepository.get_repository()
    await user_course_repo.update_with_push(
        UserCourseEntity(
            user_id=user_id,
            course_id=course_id,
            is_archived=True
        )
    )


async def update_user_course_service(user_course_entity: UserCourseEntity) -> None:
    user_course_repo = await UserCourseRepository.get_repository()
    await user_course_repo.update_with_push(user_course_entity)
