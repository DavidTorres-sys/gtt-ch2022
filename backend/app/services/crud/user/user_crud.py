# Local imports
from app.models.user import User
from app.services.crud.crud_service import BASECrud


class UserCrud(BASECrud):
    def __init__(self, model=User):
        super().__init__(model)
    
    def _read_by_email(self, db, email):
        """
            Retrieve a user by email.

            Args:
            - db (Session): Database session.
            - email: Email of the user to retrieve.

            Returns:
            - The retrieved user or None if not found.
        """
        return db.query(self.model).filter(self.model.email == email).first()

user_crud = UserCrud()
