from exceptions.base import BaseServerException


class GoogleOAuthError(BaseServerException):
    status_code = 401
    message = 'Invalid credentials'
