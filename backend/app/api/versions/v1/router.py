# FastAPI imports
from fastapi import APIRouter
# Local imports
from app.api.versions.v1.routes import dog, user

api_route = APIRouter()

api_route.include_router(dog.router, prefix="/dog", tags=["dog"])
api_route.include_router(user.router, prefix="/user", tags=["user"])
