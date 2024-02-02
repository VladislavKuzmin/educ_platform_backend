from exceptions.base import BaseServerException


class TestNotFound(BaseServerException):
    status_code = 404
    message = 'Test not found'
