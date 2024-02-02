# FastAPI instance
from fastapi import FastAPI
# Local imports
from . import models
from app.utils.database import get_db
from app.db.database import engine
from app.api.versions.v1.router import api_route

# Create the FastAPI instance
app = FastAPI()
# Create tables if they do not exist
models.Base.metadata.create_all(bind=engine)
# Dependency to get the database session
app.dependency_overrides[get_db] = get_db
app.include_router(api_route, prefix="/v1")
