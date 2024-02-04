# Pydantic Imports
from pydantic import BaseModel, Field, SecretStr
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
        max_length=50,
    )


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: int
    created_date: datetime
    hashed_password: SecretStr

    class Config:
        orm_mode = True


class UserResponse(UserInDB):
    dog: Optional[List[DogResponse]]
