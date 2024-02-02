# Pydantic imports
from pydantic import BaseModel
# Typing imports
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str
    expires: int


class TokenPayload(BaseModel):
    sub: Union[int, str, None] = None
