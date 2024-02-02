from fastapi import Depends

from entities.user_course import UserCourseEntity
from exceptions.course import TestNotFound
from services.course import get_course_service
from services.user_courses import (
    get_assigned_course_progressions_service, get_user_courses_service, sign_up_for_course_service, update_user_course_service,
    get_user_progression_service, sign_out_from_course_service
)
from transport.handlers.user_courses.schemas import (
    GetAssignedCourseProgressionsRequestSchema, GetUserCoursesResponseSchema, GetUserCourseProgressionResponseSchema, PostUserCourseRequestSchema,
    UpdateUserCourseRequestSchema, GetUserCourseProgressionRequestSchema, GetUserCoursesRequestSchema,
    SubmitTestResponseSchema, SubmitTestRequestSchema
)
from transport.routers import client_router


@client_router.get(
    path='/learn/progression',
    summary='Получение прогрессии пользователя по курсу',
    response_model=GetUserCourseProgressionResponseSchema,
    response_model_by_alias=True,
)
async def get_user_course_progression_view(
        request: GetUserCourseProgressionRequestSchema = Depends(),
        # current_user: Annotated[UserEntity, Depends(get_current_user)]
) -> GetUserCourseProgressionResponseSchema:
    course_progression = await get_user_progression_service(user_id=request.user_id, course_id=request.course_id)
    return course_progression.to_api_schema(GetUserCourseProgressionResponseSchema)


@client_router.get(
    path='/learn/progressions',
    summary='Получение всех курсов для пользователя',
    response_model=GetUserCoursesResponseSchema,
    response_model_by_alias=True,
)
async def get_user_courses_view(
        request: GetUserCoursesRequestSchema = Depends(),
        # current_user: Annotated[UserEntity, Depends(get_current_user)]
) -> GetUserCoursesResponseSchema:
    courses = await get_user_courses_service(user_id=request.user_id)
    return GetUserCoursesResponseSchema(
        items=[course.to_api_schema(GetUserCourseProgressionResponseSchema) for course in courses])


@client_router.get(
    path='/learn/assigned',
    summary='Получение прогрессий курса, назначенных пользователем',
    response_model=GetUserCoursesResponseSchema,
    response_model_by_alias=True,
)
async def get_user_assigned_courses_view(
        request: GetAssignedCourseProgressionsRequestSchema = Depends(),
        # current_user: Annotated[UserEntity, Depends(get_current_user)]
):
    progressions = await get_assigned_course_progressions_service(
        course_id=request.course_id,
        assigned_by=request.assigned_by
    )
    return GetUserCoursesResponseSchema(
        items=[progression.to_api_schema(GetUserCourseProgressionResponseSchema) for progression in progressions]
    )
    

@client_router.post(
    path='/learn/sign-up',
    summary='Записаться на курс',
    status_code=201
)
async def sign_up_for_course_view(
        request: PostUserCourseRequestSchema,
):
    await sign_up_for_course_service(
        user_id=request.user_id,
        course_id=request.course_id,
        assigned_by=request.assigned_by
    )


@client_router.post(
    path='/learn/sign-out',
    summary='Выйти с курса',
    status_code=200
)
async def sign_out_from_course_view(
        request: PostUserCourseRequestSchema,
):
    await sign_out_from_course_service(user_id=request.user_id, course_id=request.course_id)


@client_router.patch(
    path='/learn/update-progression',
    summary='Обновить данные курса',
    status_code=201
)
async def update_user_course_view(
        request: UpdateUserCourseRequestSchema,
        # current_user: Annotated[UserEntity, Depends(get_current_user)]
):
    print(request.model_dump())
    user_course_entity = UserCourseEntity.from_api_schema(schema=request)

    await update_user_course_service(user_course_entity=user_course_entity)


@client_router.post(
    path='/learn/submit-test',
    summary='Проверить результат теста',
    status_code=200
)
async def submit_test_view(
        request: SubmitTestRequestSchema,
        # current_user: Annotated[UserEntity, Depends(get_current_user)]
):
    course = await get_course_service(course_id=request.course_id)

    for chapter in course.chapters:
        for subchapter in chapter.sub_chapters:
            if subchapter.index == request.subchapter_id:

                questions = subchapter.content.data.questions
                if questions is None:
                    raise TestNotFound()
                
                correct_answers: list[list[int]] = []
                for question in questions:
                    correct_answers.append(question.answers)

                if len(correct_answers) != len(request.answers):
                    raise TestNotFound()

                print('correct', correct_answers)
                print('request', request.answers)

                answered_correctly: list[int] = []
                for i in range(len(questions)):
                    if correct_answers[i] == request.answers[i]:
                        answered_correctly.append(i)

                return SubmitTestResponseSchema(answered_correctly=answered_correctly)
            