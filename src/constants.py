from enum import StrEnum

from settings import get_settings

settings = get_settings()


class ContentType(StrEnum):
    TEXT = 'info'
    VIDEO = 'video'
    TEST = 'test'


class CourseTag(StrEnum):
    PYTHON = 'python'
    JAVA_SCRIPT = 'java_script'
    WEB_DEVELOPMENT = 'web_development'
    DATA_SCIENCE = 'data_science'
    MOBILE_DEVELOPMENT = 'mobile_development'
    QA_AUTOMATION = 'qa_automation'
