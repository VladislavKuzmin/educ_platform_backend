from typing import Optional


class BaseServerException(Exception):
    status_code: Optional[int] = 500
    message: Optional[str] = 'Что-то пошло не так'

    def __init__(
            self,
            status_code: Optional[int] = None,
            message: Optional[str] = None,
            debug: Optional[str] = None,
            exc_code: Optional[str] = None,
    ):
        self.status_code = status_code or self.status_code
        self.message = message or self.message
        self.debug = debug
        self.code = exc_code or self.__class__.__name__
        super(Exception, self).__init__(message)
