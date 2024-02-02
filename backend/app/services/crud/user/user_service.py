# FastAPI imports
from fastapi import status, HTTPException
# SQLAlchemy imports
from sqlalchemy.orm import Session
# Typing imports
from typing import List
from datetime import timedelta
# Local imports
from app.schemas.user import UserResponse, UserUpdate, UserCreate, UserInDB
from app.services.security import jwt_token
from .user_crud import user_crud


class UserService():

    def read_all(self, db: Session, skip: int, limit: int) -> List[UserResponse]:
        """
            Retrieve a list of users from the database.

            Args:
            - db (Session): Database session.
            - skip (int): Number of records to skip.
            - limit (int): Maximum number of records to retrieve.

            Returns:
            - List[UserResponse]: A list of user records.

            Raises:
            - HTTPException 404 Not Found: If no users are found in the specified range.
            - HTTPException 500 Internal Server Error: If an unexpected error occurs during the database operation.
        """
        try:
            db_objs = user_crud._read_all(db, skip, limit)
            if not db_objs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
            return db_objs
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def create(self, db: Session, obj_in: UserCreate) -> UserResponse:
        """
            Create a new user in the database.

            Args:
            - db (Session): Database session.
            - obj_in (UserCreate): Input data for creating a new user.

            Returns:
            - The user created.

            Raises:
            - HTTPException 400 Bad Request: If the provided email is already registered.
            - HTTPException 500 Internal Server Error: If an unexpected error occurs during the database operation.
        """
        # Check if the email is already registered
        existing_obj = user_crud._read_by_email(db, obj_in.email)
        if existing_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        try:
            db_obj = user_crud._create(db, obj_in)
            db_obj.name = db_obj.name.lower()
            db_obj.last_name = db_obj.last_name.lower()

            # Generate a JWT token for the created user
            expires_delta = timedelta(minutes=15)
            token = jwt_token.create_jwt_token({"sub": db_obj.id}, expires_delta)

            return self._generate_user_response(db_obj, token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, db: Session, obj_id: int, obj_in: UserUpdate) -> UserResponse:
        """
            Update a user in the database.

            Args:
            - db (Session): Database session.
            - obj_id (int): ID of the user to be updated.
            - obj_in: (UserUpdate) Input data for updating the user.

            Returns:
            - The updated user.

            Raises:
            - HTTPException 404 Not Found: If the user with the specified ID is not found.
            - HTTPException 500 Internal Server Error: If an unexpected error occurs during the database operation.
        """
        # Check if the user exists in the database
        existing_obj = user_crud._read(db, obj_id)
        if not existing_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        try:
            return user_crud._update(db, obj_id, obj_in)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete(self, db: Session, obj_id: int):
        """
            Delete an existing user from the database.

            Args:
            - db (Session): Database session.
            - obj_id (int): ID of the user to be deleted.

            Returns:
            - The deleted user.

            Raises:
            - HTTPException 404 Not Found: If the user with the specified ID is not found.
            - HTTPException 500 Internal Server Error: If an unexpected error occurs during the database operation.
        """
        # Check if the user exists in the database
        existing_obj = user_crud._read(db, obj_id)
        if not existing_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        try:
            return user_crud._delete(db, obj_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def read(self, db: Session, obj_id: int) -> UserResponse:
        """
            Retrieve a user by ID from the database.

            Args:
            - db (Session): Database session.
            - obj_id (int): ID of the user to_ be retrieved.

            Returns:
            - The retrieved user.

            Raises:
            - HTTPException 404 Not Found: If the user with the specified ID is not found.
            - HTTPException 500 Internal Server Error: If an unexpected error occurs during the database operation.
        """
        try:
            db_obj = user_crud._read(db, obj_id)
            if not db_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def _generate_user_response(self, user_obj: UserInDB, jwt_token: str) -> UserResponse:
        return UserResponse.from_orm(user_obj).copy(update={"jwt_token": jwt_token, "dog": []})


user_service = UserService()
