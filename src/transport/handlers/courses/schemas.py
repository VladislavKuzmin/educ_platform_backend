from typing import Literal, Optional

from constants import ContentType
from transport.base_api_schema import BaseApiSchema


class _Info(BaseApiSchema):
    html: str


class _Tag(BaseApiSchema):
    group_name: Literal["difficulty", "language", "specification"]
    value: str


class _Question(BaseApiSchema):
    question: str
    type: Literal['select-one', 'select-many', 'compare']
    options: list[str]
    answers: list[int]


class _Test(BaseApiSchema):
    questions: list[_Question]


class _Video(BaseApiSchema):
    source: str


class _Content(BaseApiSchema):
    type: ContentType
    data: _Info | _Test | _Video


class _CourseSubChapter(BaseApiSchema):
    index: int
    title: str
    content: _Content


class _CourseChapter(BaseApiSchema):
    index: int
    title: str
    sub_chapters: list[_CourseSubChapter]


class PostCourseRequestSchema(BaseApiSchema):
    title: str
    tags: list[_Tag]
    description: str
    preview_html: str
    estimation: int
    chapters: list[_CourseChapter]
    empty_test_answers: dict[str, list[list[int]]]


class GetFullCourseRequestSchema(BaseApiSchema):
    id: str


class GetFullCourseResponseSchema(BaseApiSchema):
    id: str
    title: str
    tags: list[_Tag]
    description: str
    estimation: int
    chapters: list[_CourseChapter]
    empty_test_answers: dict[int, list[list[int]]]


class CourseCard(BaseApiSchema):
    id: str
    title: str
    tags: list[_Tag]
    description: str
    estimation: int
    total_subchapters: int


class GetCoursesCardsRequestSchema(BaseApiSchema):
    ids: Optional[str] = None


class GetCoursesCardsResponseSchema(BaseApiSchema):
    items: list[CourseCard]


class GetCourseDemoRequestSchema(BaseApiSchema):
    course_id: str
    user_id: Optional[str] = None


class CoursePreview(BaseApiSchema):
    id: str
    title: str
    tags: list[_Tag]
    preview_html: str
    estimation: int


class GetCourseDemoResponseSchema(BaseApiSchema):
    preview: CoursePreview
    is_studying: bool
