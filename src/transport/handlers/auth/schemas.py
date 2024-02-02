from typing import Optional

from pydantic import BaseModel


class LoginCallbackSchema(BaseModel):
    code: str = None
    error: Optional[str] = None
