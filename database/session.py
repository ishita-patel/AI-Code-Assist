from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Use the DATABASE_URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)