import pprint
from asyncio import gather

from fastapi import Depends

from entities.course import CourseEntity
from services.course import create_course_service, get_course_service, get_courses_cards_service
from services.user_courses import get_user_progression_service
from transport.handlers.courses.schemas import (
    PostCourseRequestSchema, GetFullCourseRequestSchema,
    GetFullCourseResponseSchema, GetCoursesCardsResponseSchema, CourseCard, GetCourseDemoRequestSchema,
    GetCourseDemoResponseSchema, CoursePreview, GetCoursesCardsRequestSchema
)
from transport.routers import client_router


@client_router.post(
    path='/course',
    summary='Создание курса',
    status_code=200
)
async def post_course_view(
        request: PostCourseRequestSchema,
):
    pprint.pprint(request)
    await create_course_service(course_entity=CourseEntity.from_api_schema(schema=request))


@client_router.get(
    path='/course',
    summary='Получение полных данных курса',
    response_model=GetFullCourseResponseSchema,
    response_model_by_alias=True
)
async def get_full_course_view(
        request: GetFullCourseRequestSchema = Depends(),
) -> GetFullCourseResponseSchema:
    course = await get_course_service(course_id=request.id)
    return course.to_api_schema(GetFullCourseResponseSchema)


@client_router.get(
    path='/course/cards',
    summary='Получение карточек курсов',
    response_model=GetCoursesCardsResponseSchema,
    response_model_by_alias=True
)
async def get_courses_cards_view(
        request: GetCoursesCardsRequestSchema = Depends(),
) -> GetCoursesCardsResponseSchema:
    result = await get_courses_cards_service(request.ids)

    return GetCoursesCardsResponseSchema(
        items=[course.to_api_schema(CourseCard) for course in result],
    )


@client_router.get(
    path='/course/demo',
    summary='Получение превью курса',
    response_model=GetCourseDemoResponseSchema,
    response_model_by_alias=True
)
async def get_course_view(
        request: GetCourseDemoRequestSchema = Depends(),
) -> GetCourseDemoResponseSchema:
    course = await get_course_service(course_id=request.course_id)
    if request.user_id:
        progression = await get_user_progression_service(user_id=request.user_id, course_id=request.course_id)
    else:
        progression = None

    return GetCourseDemoResponseSchema(
        preview=course.to_api_schema(CoursePreview),
        is_studying=True if progression else False
    )
