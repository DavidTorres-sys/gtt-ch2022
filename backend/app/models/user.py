# SQLAlchemy imports
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# Local imports
from app.db.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String)
    created_date = Column(DateTime, default=func.now())
    # Relationship
    dog = relationship("Dog", back_populates="user")
