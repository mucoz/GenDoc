from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DatabaseSession:
    """
    A class to manage database sessions and configurations.
    """
    def __init__(self, db_path: str):
        # Ensure the directory for the database exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # Construct the SQLite database URL
        self.database_url = f"sqlite:///{db_path}"
        self.engine = create_engine(
            self.database_url, connect_args={"check_same_thread": False}  # SQLite-specific argument
        )
        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        self.Base = declarative_base()

    def get_db(self):
        """
        Provides a database session. Automatically handles session closing.
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_engine(self):
        return self.engine
