from exceptions.base import BaseServerException


class UserNotFound(BaseServerException):
    status_code = 404
    message = 'User not found'


