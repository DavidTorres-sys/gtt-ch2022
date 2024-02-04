import httpx
# FastAPI imports
from fastapi import APIRouter, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse
# Typing imports
from typing import List, Any
# Local imports
from app.utils.database import get_db
from app.schemas.dog import DogResponse, DogCreate, DogUpdate
from app.services.crud.dog import dog_service
from app.api.middlewares.jwt_bearer import oauth2_scheme

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[DogResponse])
async def read_all(
        *,
        db_session=Depends(get_db),
        skip: int = Query(0, description="Number of registers to skip (for pagination)."),
        limit: int = Query(10, description="Maximum number of registers to retrieve (for pagination).")):
    """
        Endpoint to retrieve a list of dogs with optional pagination.

        Params:
        - db_session: Database session.
        - skip: Number of registers to skip.
        - limit: Maximum number of registers to retrieve.

        Returns:
        - List of retrieved dogs(DogResponse).
    """
    db_dogs = dog_service.read_all(db_session, skip, limit)
    return db_dogs


@router.get("/{dog_id}", status_code=status.HTTP_200_OK, response_model=DogResponse)
async def read_dog(
        *,
        db_session=Depends(get_db),
        dog_id: int):
    """
        Endpoint to retrieve a dog by ID.

        Params:
        - db_session: Database session.
        - dog_id: Dog ID.

        Returns:
        - DogResponse.
    """
    db_dog = dog_service.read_by_id(db_session, dog_id)
    return db_dog


@router.get("/name/{dog_name}", status_code=status.HTTP_200_OK, response_model=DogResponse)
async def read_name(
        *,
        db_session=Depends(get_db),
        dog_name: str):
    """
        Endpoint to retrieve a dog by name.

        Params:
        - db_session: Database session.
        - dog_name: Dog name.

        Returns:
        - DogResponse.
    """
    db_dog = dog_service.read_by_name(db_session, dog_name.lower())
    return db_dog


@router.get("/is_adopted/", status_code=status.HTTP_200_OK, response_model=List[DogResponse])
async def read_adopted(
        *,
        db_session=Depends(get_db),
        is_adopted: bool = Query(True, description="Filter by adopted status.")):
    """
        Endpoint to retrieve a list of adopted dogs.

        Params:
        - db_session: Database session.

        Returns:
        - List of retrieved dogs(DogResponse).
    """
    db_dogs = dog_service.read_all_adopted(db_session, is_adopted)
    return db_dogs


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DogResponse)
async def create_dog(
        *,
        db_session=Depends(get_db),
        current_user: str = Depends(oauth2_scheme),
        dog_in: DogCreate):
    """
        Endpoint to create a dog.

        Params:
        - db_session: Database session.
        - jwt_token: JWT token obtained from the header.
        - dog_in: DogResponse.

        Returns:
        - DogResponse.
    """
    db_dog = dog_service.create(db_session, dog_in)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://dog.ceo/api/breeds/image/random")
            response.raise_for_status()
            db_dog.picture = response.json()["message"]
            db_session.commit()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error getting image: {e}",
            )
    return db_dog


@router.put("/{dog_id}", status_code=status.HTTP_200_OK, response_model=DogResponse)
async def update_dog(
        *,
        db_session=Depends(get_db),
        dog_id: int,
        dog_in: DogUpdate):
    """
        Endpoint to update a dog.

        Params:
        - db_session: Database session.
        - dog_id: Dog ID.
        - dog_in: DogResponse.

        Returns:
        - DogResponse.
    """
    db_dog = dog_service.update(db_session, dog_id, dog_in)
    return db_dog


@router.put("/name/{dog_name}", status_code=status.HTTP_200_OK, response_model=DogResponse)
async def update_dog_by_name(
        *,
        db_session=Depends(get_db),
        dog_name: str,
        dog_in: DogUpdate):
    """
        Endpoint to update a dog by name.

        Params:
        - db_session: Database session.
        - dog_name: Dog name.
        - dog_in: DogResponse.

        Returns:
        - DogResponse.
    """
    db_dog = dog_service.update_by_name(db_session, dog_name.lower(), dog_in)
    return db_dog


@router.delete("/{dog_id}", status_code=status.HTTP_200_OK, response_model=Any)
async def delete_by_id(
        *,
        db_session=Depends(get_db),
        dog_id: int):
    """
        Endpoint to delete a dog.

        Params:
        - db_session: Database session.
        - dog_id: Dog ID.

        Returns:
        - Any.
    """
    db_dog = dog_service.delete(db_session, dog_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'Dog deleted'
    })


@router.delete("/name/{dog_name}", status_code=status.HTTP_200_OK, response_model=Any)
async def delete_by_name(
        *,
        db_session=Depends(get_db),
        dog_name: str):
    """
        Endpoint to delete a dog by name.

        Params:
        - db_session: Database session.
        - dog_name: Dog name.

        Returns:
        - Any.
    """
    db_dog = dog_service.delete_by_name(db_session, dog_name.lower())
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'detail': 'Dog deleted'
    })
