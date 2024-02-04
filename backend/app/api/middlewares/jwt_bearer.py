# FastAPI imports
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# Typing imports
from typing import Annotated
# Local imports
from app.services.security import jwt_token
from app.utils.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"http://localhost:8000/v1/user/access-token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session=Depends(get_db)):
    """
    Get the current user's information from a JSON Web Token (JWT).

    Parameters:
    - token (str): The JWT token obtained from the request header.

    Returns:
    - TokenPayload: The payload of the decoded and validated JWT, representing the current user's information.
    """
    return jwt_token.decode_token(db_session, token)
