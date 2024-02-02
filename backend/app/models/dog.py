# SQLAlchemy imports
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
# Local imports
from app.db.database import Base


class Dog(Base):
    __tablename__ = "dog"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    picture = Column(String)
    is_adopted = Column(Boolean)
    created_date = Column(DateTime, default=func.now())
    # Relationship
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="dog")
