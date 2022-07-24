"""
Database dependencies
"""
from app.database.connection import SessionLocal
from app.database.connection import engine

def get_db():
    """
    Dependency to inject database session to controller
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
