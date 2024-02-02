from exceptions.base import BaseServerException


class FileNotFound(BaseServerException):
    status_code = 404
    message = 'File not found'

