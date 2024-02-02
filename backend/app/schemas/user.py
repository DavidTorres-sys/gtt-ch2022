# Pydantic Imports
from pydantic import BaseModel, Field
# Typing imports
from datetime import datetime
from typing import List, Optional
# Local imports
from .dog import DogResponse


class UserBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        min_length=1,
        max_length=50,
    )
    email: str = Field(
        min_length=1,
        max_length=100,
    )


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True


class UserResponse(UserInDB):
    jwt_token: Optional[str]
    dog: Optional[List[DogResponse]]
