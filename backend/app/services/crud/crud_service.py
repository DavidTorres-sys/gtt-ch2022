# FastAPI imports
from fastapi import status, HTTPException
# SQLAlchemy imports
from sqlalchemy.orm import Session


class BASECrud:
    """
        Base CRUD class with default methods.
    """

    def __init__(self, model):
        self.model = model

    def _create(self, db: Session, obj_in):
        """
            Create a new database register.

            Args:
            - db (Session): Database session.
            - obj_in: Input data for creating a new record.

            Returns:
            - The newly created database record.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            db_obj = self.model(**obj_in.dict())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def _read(self, db: Session, obj_id):
        """
            Retrieve a database register by ID.

            Args:
            - db (Session): Database session.
            - obj_id: ID of the record to retrieve.

            Returns:
            - The retrieved database register or None if not found.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            return db.query(self.model).filter(self.model.id == obj_id).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def _update(self, db: Session, obj_id, obj_in):
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
        try:
            db_obj = db.query(self.model).filter(
                self.model.id == obj_id).first()
            for field, value in obj_in.dict().items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def _delete(self, db: Session, obj_id):
        """
            Delete a database register by ID.

            Args:
            - db (Session): Database session.
            - obj_id: ID or name (or any unique identifier) of the register to delete.

            Returns:
            - The deleted database register.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            db_obj = db.query(self.model).filter(
                self.model.id == obj_id).first()
            db.delete(db_obj)
            db.commit()
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def _read_all(self, db: Session, skip: int = 0, limit: int = 10):
        """
            Retrieve a list of database register with optional pagination.

            Args:
            - db (Session): Database session.
            - skip (int): Number of register to skip (for pagination).
            - limit (int): Maximum number of register to retrieve (for pagination).

            Returns:
            - List of retrieved database register.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
