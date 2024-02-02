import os
# Import statements for SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# dotenv imports
from dotenv import load_dotenv

load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")
# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Declarative base for SQLAlchemy models
Base = declarative_base()
