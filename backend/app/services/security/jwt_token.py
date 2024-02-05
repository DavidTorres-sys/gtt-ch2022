import os
# FastAPI imports
from fastapi import HTTPException, status
# SQLAlchemy imports
from sqlalchemy.orm import Session
# Passlib imports
from passlib.context import CryptContext
# PyJWT imports
from jose import JWTError, jwt
# Typing imports
from datetime import datetime, timedelta, timezone
from typing import Union
# dotenv imports
from dotenv import load_dotenv
# Local imports
from app.models.user import User

load_dotenv()
# Secret key to sign the JWT token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JwtToken():
    def create_jwt_token(self, data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        """
            Create a JSON Web Token (JWT) with the specified data and expiration time.

            Parameters:
            - data (dict): The payload data to be included in the JWT.
            - expires_delta (timedelta): The duration of time after which the JWT will expire.

            Returns:
            - str: The generated JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + \
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, db, token: str):
        """
            Decode and validate a JSON Web Token (JWT) to obtain its payload.

            Parameters:
            - token (str): The JWT token to be decoded and validated.

            Raises:
            - HTTPException 401 Unauthorized: If the token is invalid or expired.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            decoded_token = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM])
            email = decoded_token.get("sub")
            if email is None:
                raise credentials_exception
            token_data = {"sub": email}
        except JWTError:
            raise credentials_exception
        user = self.get_user(db, email=token_data.email)
        return user

    def verify_password(self, plain_password, hashed_password) -> bool:
        """
            Verify if the provided plain password matches the hashed password.

            Parameters:
            - plain_password (str): The plain text password to verify.
            - hashed_password (str): The hashed password to compare against.

            Returns:
            - bool: True if the passwords match, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        """
            Generate a secure hashed version of the provided password.

            Parameters:
            - password (str): The password to hash.

            Returns:
            - str: The hashed password.
        """
        return pwd_context.hash(password)
    
    def get_user(self, db: Session, email: str):
        """
            Get a user by email.

            Parameters:
            - db (Session): Database session.
            - email (str): Email of the user to retrieve.

            Returns:
            - User: The user with the specified email.
        """
        return db.query(User).filter(User.email == email).first()

    def authenticate_user(self, db: Session, email: str, password: str):
        """
        Authenticate a user.

        Parameters:
        - db (Session): Database session.
        - email (str): Email of the user attempting to log in.
        - password (str): Password provided by the user.

        Returns:
        - UserResponse.

        """
        # Check if the user exists in the database
        existing_user = self.get_user(db, email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Check if the password is correct
        if not self.verify_password(password, existing_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email")
        return existing_user


jwt_token = JwtToken()
