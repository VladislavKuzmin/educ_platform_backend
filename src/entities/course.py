from typing import Optional, Literal

from pydantic import BaseModel

from constants import ContentType
from entities.base import BaseEntity
from repositories.models.course import CourseDBModel


class Info(BaseModel):
    html: Optional[str]


class Tag(BaseModel):
    group_name: Literal["difficulty", "language", "specification"]
    value: str


class Question(BaseModel):
    question: Optional[str] = None
    type: Literal['select-one', 'select-many', 'compare'] | None = None
    options: Optional[list[str]] = None
    answers: Optional[list[int]] = None


class Test(BaseModel):
    questions: Optional[list[Question]]


class Video(BaseModel):
    source: Optional[str]


class Content(BaseModel):
    type: Optional[ContentType] = None
    data: Info | Test | Video | None = None


class CourseSubChapter(BaseModel):
    index: Optional[int] = None
    title: Optional[str] = None
    content: Optional[Content] = None


class CourseChapter(BaseModel):
    index: Optional[int] = None
    title: Optional[str] = None
    sub_chapters: Optional[list[CourseSubChapter]] = None


class CourseEntity(BaseEntity):
    _DB_MODEL = CourseDBModel

    title: Optional[str] = None
    tags: Optional[list[Tag]] = None
    description: Optional[str] = None
    preview_html: Optional[str] = None
    estimation: Optional[int] = None
    chapters: Optional[list[CourseChapter]] = None
    total_subchapters: Optional[int] = 0
    empty_test_answers: Optional[dict[str, list[list[int]]]] = None
