# FastAPI imports
from fastapi import status, HTTPException
# SQLAlchemy imports
from sqlalchemy.orm import Session
# Local imports
from .dog_crud import dog_crud


class DogService():

    def read_all(self, db: Session, skip: int, limit: int):
        """
            Retrieve a list of database registers with optional pagination.

            Args:
            - db (Session): Database session.
            - skip (int): Number of registers to skip (for pagination).
            - limit (int): Maximum number of registers to retrieve (for pagination).

            Returns:
            - List of retrieved database registers.
        """
        db_objs = dog_crud._read_all(db, skip, limit)
        if not db_objs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No dogs found")
        return db_objs

    def read_by_id(self, db: Session, obj_id):
        """
            Retrieve a database register by ID.

            Args:
            - db (Session): Database session.
            - obj_id: ID of the register to retrieve.

            Returns:
            - The retrieved database register or None if not found.
        """
        db_obj = dog_crud._read(db, obj_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dog not found")
        return db_obj

    def read_by_name(self, db: Session, obj_name: str):
        """
            Retrieve a database register by name.

            Args:
            - db (Session): Database session.
            - obj_id: Name of the register to retrieve.

            Returns:
            - The retrieved database register or None if not found.
        """
        db_obj = dog_crud._read_by_name(db, obj_name)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dog not found")
        return db_obj

    def read_all_adopted(self, db: Session, is_adopted: bool):
        """
            Retrieve a list of adopted database register.

            Args:
            - db (Session): Database session.

            Returns:
            - List of retrieved database register marked as adopted.
        """
        db_objs = dog_crud._read_all_adopted(db, is_adopted)
        if not db_objs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No dogs found")
        return db_objs

    def create(self, db: Session, obj_in):
        """
            Create a new database record.

            Args:
            - db (Session): Database session.
            - obj_in: Input data for creating a new register.

            Returns:
            - The newly created database register.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            db_obj = dog_crud._create(db, obj_in)
            db_obj.name = db_obj.name.lower()
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update(self, db: Session, obj_id, obj_in):
        """
            Update a database register by ID.

            Args:
            - db (Session): Database session.
            - obj_id: ID of the register to update.
            - obj_in: Input data for updating the register.

            Returns:
            - The updated database register.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        existing_obj = dog_crud._read(db, obj_id)
        if not existing_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dog not found")
        try:
            return dog_crud._update(db, obj_id, obj_in)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_by_name(self, db: Session, obj_name: str, obj_in):
        """
            Update a database register by name.

            Args:
            - db (Session): Database session.
            - obj_name: Name of the register to update.
            - obj_in: Input data for updating the register.

            Returns:
            - The updated database register.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        existing_obj = dog_crud._read_by_name(db, obj_name)
        if not existing_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dog not found")
        try:
            return dog_crud._update_by_name(db, obj_name, obj_in)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete(self, db: Session, obj_id):
        """
            Delete a database record by ID.

            Args:
            - db (Session): Database session.
            - obj_id: ID of the record to delete.

            Returns:
            - The deleted database record.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        existing_obj = dog_crud._read(db, obj_id)
        if not existing_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dog not found")
        try:
            return dog_crud._delete(db, obj_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_by_name(self, db: Session, obj_name: str):
        """
            Delete a database record by name.

            Args:
            - db (Session): Database session.
            - obj_name: Name of the record to delete.

            Returns:
            - The deleted database record.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        existing_obj = dog_crud._read_by_name(db, obj_name)
        if not existing_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dog not found")
        try:
            return dog_crud._delete_by_name(db, obj_name)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


dog_service = DogService()
