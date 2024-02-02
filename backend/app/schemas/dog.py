# Pydantic imports
from pydantic import BaseModel, Field
# Typing imports
from typing import Optional
from datetime import datetime


class DogBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )
    is_adopted: bool


class DogCreate(DogBase):
    pass


class DogUpdate(DogBase):
    pass


class DogInDB(DogBase):
    id: int
    created_date: datetime
    picture: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


class DogResponse(DogInDB):
    pass
