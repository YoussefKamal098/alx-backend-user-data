#!/usr/bin/env python3
"""
Database management class using SQLAlchemy.
"""
from threading import Lock
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

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

        # Create a sessionmaker factory
        self.__session_factory = sessionmaker(bind=self._engine)

    def _initialize_db(self) -> None:
        """
        Initialize the database schema (tables) by creating them.
        """
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    @property
    def _session(self) -> scoped_session:
        """
        Returns a session object. It ensures each thread gets
        a separate session.
        """
        # Using scoped_session to ensure thread-local session management
        return scoped_session(self.__session_factory)

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
        session = self._session()  # Get a session instance per thread

        try:
            user = User(email=email, hashed_password=hashed_password)
            session.add(user)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            user = None
        finally:
            self._session.remove()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first matching user object.

        Raises:
            NoResultFound: If no matching user is found.
            InvalidRequestError: If the query arguments are invalid.
        """
        session = self._session()  # Get a session instance per thread

        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found matching the criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments provided.")
        finally:
            self._session.close()

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates an existing user in the database based on the provided user_id
        and the given keyword arguments. The method finds the user by
        the provided user_id, and updates the user's attributes with the
        values provided in **kwargs. If an invalid attribute is provided in
        **kwargs, a ValueError is raised. The changes are committed to the
        database, and any errors during the update result in a rollback.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments
                representing the attributes to update.

        Raises:
            ValueError: If an invalid attribute is provided in **kwargs.
            InvalidRequestError: If there is an issue with the update request.

        Returns:
            None: The method does not return any value.
        """
        session = self._session()

        user = self.find_user_by(id=user_id)
        if not user:
            return

        try:
            session.query(User).filter_by(id=user_id).\
                update(kwargs, synchronize_session=False)
            session.commit()
        except InvalidRequestError as err:
            session.rollback()
            raise ValueError(err)
        finally:
            self._session.close()

    def close(self) -> None:
        """
        Dispose the engine and clean up session management.
        """
        self._session.remove()
        self._engine.dispose()
