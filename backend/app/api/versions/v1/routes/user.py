import os
# FastAPI imports
from fastapi import APIRouter, Depends, status, Query, Path
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
# Typing imports
from typing import List, Any
# dotenv imports
from dotenv import load_dotenv
# Local imports
from app.utils.database import get_db
from app.schemas.user import UserResponse, UserUpdate, UserCreate
from app.schemas.token import Token
from app.services.crud.user import user_service
from app.services.security import jwt_token

router = APIRouter()

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def read_all(
        *,
        db_session=Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)):
    """
        Endpoint to read all users.

        Params:
        - skip: Number of users to skip (non-negative integer)
        - limit: Number of users to read and return (between 1 and 100)
        Dependencies:
        - db_session: SQLAlchemy database session.
        Returns:
        - users: List of UserResponse
    """
    db_users = user_service.read_all(db_session, skip, limit)
    return db_users


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def read_user(
        *,
        db_session=Depends(get_db),
        user_id: int = Path(..., title="The ID of the user to retrieve", gt=0)):
    """
        Endpoint to read a user by id.

        Params:
        - user_id: User id
        Dependencies:
        - db_session: SQLAlchemy database session.
        Returns:
        - user: UserResponse
    """
    db_user = user_service.read(db_session, user_id)
    return db_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
        *,
        db_session=Depends(get_db),
        user_in: UserCreate):
    """
        Endpoint to create a user.

        Params:
        - user_in: UserResponse
        Dependencies:
        - db_session: SQLAlchemy database session.
        Returns:
        - user: UserResponse
    """
    return user_service.create(db_session, user_in)


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(
        *,
        db_session=Depends(get_db),
        user_id: int,
        user_in: UserUpdate):
    """
        Endpoint to update a user.

        Params:
        - user_id: User id
        - user_in: UserResponse
        Dependencies:
        - db_session: SQLAlchemy database session.
        Returns:
        - user: UserResponse
    """
    db_user = user_service.update(db_session, user_id, user_in)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=Any)
async def delete_user(
        *,
        db_session=Depends(get_db),
        user_id: int):
    """
        Endpoint to delete a user.

        Params:
        - user_id: User.id
        Dependencies:
        - db_session: SQLAlchemy database session.
        Returns:
        - mgs: str
    """
    db_user = user_service.delete(db_session, user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'User deleted'
    })


@router.post("/access-token", status_code=status.HTTP_200_OK)
async def access_token(
        *,
        db_session=Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    """
        Endpoint to obtain an access token.

        Dependencies:
        - form_data: OAuth2PasswordRequestForm

        Returns:
        - JSONResponse: JSON response containing the access token.
    """
    user = jwt_token.authenticate_user(db_session, form_data.username, form_data.password)
    access_token = jwt_token.create_jwt_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer", expires=ACCESS_TOKEN_EXPIRE_MINUTES)
    
