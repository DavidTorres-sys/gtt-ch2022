# FastAPI imports
from fastapi import HTTPException, status
# SQLAlchemy model imports
from sqlalchemy.orm import Session
# Local imports
from app.models.dog import Dog
from app.services.crud.crud_service import BASECrud


class DogCrud(BASECrud):
    """
        CRUD for Dog. this class inherits from the superclass BASECrud.
    """

    def __init__(self, model=Dog):
        super().__init__(model)

    def _read_by_name(self, db: Session, name: str):
        """
            Retrieve a database register by name.

            Args:
            - db (Session): Database session.
            - name (str): Name of the register to retrieve.

            Returns:
            - The retrieved database register or None if not found.
        """
        return db.query(self.model).filter(self.model.name.ilike(name)).first()

    def _read_all_adopted(self, db: Session, is_adopted: bool):
        """
            Retrieve a list of database register that are marked as adopted.

            Args:
            - db (Session): Database session.

            Returns:
            - List of retrieved database register marked as adopted.
        """
        return db.query(self.model).filter(self.model.is_adopted == is_adopted).all()

    def _update_by_name(self, db: Session, name: str, obj_in):
        """
            Update the name of a database register by ID.

            Args:
            - db (Session): Database session.
            - obj_id: ID of the record to update.
            - name (str): New name for the record.

            Returns:
            - The updated database record.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            db_obj = db.query(self.model).filter(self.model.name.ilike(name)).first()
            for field, value in obj_in.dict().items():
                setattr(db_obj, field, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def _delete_by_name(self, db: Session, name: str):
        """
            Delete a database record by name.

            Args:
            - db (Session): Database session.
            - name (str): Name of the record to delete.

            Returns:
            - The deleted database record.

            Raises:
            - Exception: Any unexpected error during the database operation.
        """
        try:
            db_obj = db.query(self.model).filter(
                self.model.name == name).first()
            db.delete(db_obj)
            db.commit()
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


dog_crud = DogCrud()
