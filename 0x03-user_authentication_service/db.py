#!/usr/bin/env python3
"""
Database management class using SQLAlchemy.
"""
from threading import Lock
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from user import User, Base


class DB:
    """
    Thread-safe, singleton-based database manager using SQLAlchemy.

    Handles database connection, schema initialization, and user operations.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """
        Singleton pattern to ensure only one instance of DB exists.
        Thread-safe instance creation.
        """
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.__initialize("sqlite:///a.db")

        return cls._instance

    def __initialize(self, uri: str) -> None:
        """
        Initialize the database connection, create the engine with pooling,
        and set up the session factory.
        """

        # Create the engine
        self._engine = create_engine(uri)

        # Create tables if not exists
        self._initialize_db()

        # Create scoped session for thread safety
        self.__session_factory = sessionmaker(bind=self._engine)
        self._Session = scoped_session(self.__session_factory)

    def _initialize_db(self) -> None:
        """
        Initialize the database schema (tables) by creating them.
        """
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    @property
    def _session(self) -> Session:
        """
        Returns a session object. It ensures each thread gets
        a separate session.
        """
        return self._Session()

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database and commits the transaction.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            Optional[User]: The created User object,
                or None if an error occurred.
        """
        session = self._Session()

        try:
            user = User(email=email, hashed_password=hashed_password)
            session.add(user)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            user = None
        finally:
            session.close()

        return user

    def close(self) -> None:
        """
        Dispose the engine and clean up session management.
        """
        self._engine.dispose()
        self._Session.remove()
