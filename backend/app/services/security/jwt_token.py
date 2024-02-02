import os
# FastAPI imports
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# PyJWT imports
from jose import JWTError, jwt
# Typing imports
from datetime import datetime, timedelta, timezone
from typing import Union
# dotenv imports
from dotenv import load_dotenv
# Local imports
from app.schemas.token import TokenPayload

load_dotenv()
# Secret key to sign the JWT token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# OAuth2PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str = Depends(oauth2_scheme)) -> TokenPayload:
        """
            Verify a JSON Web Token (JWT) and return its payload.

            Parameters:
            - token (str): The JWT token to be verified.

            Returns:
            - dict: The payload of the verified JWT.

            Raises:
            - HTTPException: If the token is invalid or expired.
        """
        # Verifying the JWT token
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return TokenPayload(**payload)
        except JWTError:
            raise credentials_exception


jwt_token = JwtToken()
