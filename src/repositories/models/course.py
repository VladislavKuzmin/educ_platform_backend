from typing import Literal

from pydantic import BaseModel

from constants import ContentType
from repositories.models.base import BaseDBModel


class Info(BaseModel):
    html: str


class Tag(BaseModel):
    group_name: Literal["difficulty", "language", "specification"]
    value: str


class Question(BaseModel):
    question: str
    type: Literal['select-one', 'select-many', 'compare']
    options: list[str]
    answers: list[int]


class Test(BaseModel):
    questions: list[Question]


class Video(BaseModel):
    source: str


class Content(BaseModel):
    type: ContentType
    data: Info | Test | Video


class CourseSubChapter(BaseModel):
    index: int
    title: str
    content: Content


class CourseChapter(BaseModel):
    index: int
    title: str
    sub_chapters: list[CourseSubChapter]


class CourseDBModel(BaseDBModel):
    title: str
    tags: list[Tag]
    description: str
    preview_html: str
    estimation: int
    chapters: list[CourseChapter]
    total_subchapters: int
    empty_test_answers: dict[str, list[list[int]]]
