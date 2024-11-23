#!/usr/bin/env python3
"""
Password hashing and user authentication module.

This module provides functionality for securely hashing passwords using
the bcrypt algorithm and managing user authentication and registration.
It ensures secure handling of passwords by hashing them with a salt, making
it difficult to reverse-engineer the original password.

Additionally, the `Auth` class is implemented to handle user registration
and authentication, including checking if a user exists, securely hashing
their password before storing it, and validating user credentials.

Functions:
    _hash_password(password: str) -> bytes:
        Hashes the given password using bcrypt and returns the hash as a
        binary string.

    _generate_uuid() -> str:
        Generates a new UUID and returns it as a string. This function
        is private and intended for internal use to create unique
        identifiers such as session tokens.

Classes:
    Auth:
        A class responsible for user registration and authentication.
        It interacts with the database to register users, validate
        credentials, and manage user data securely.
"""

import uuid
from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
import bcrypt

from user import User
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt and returns the
    hash as a binary string.

    This method takes a plain text password, generates a random salt,
    and applies the bcrypt algorithm to hash the password. The result
    is returned in binary format.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        bytes: The hashed password in binary format,
               including the salt and the bcrypt hash.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns it as a string.

    This is a private method meant for internal use in the auth module.

    Returns:
        str: The string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the system. The email and password are
        used to create a new user entry. If a user with the same email
        already exists, raises a ValueError.

        Args:
            email (str): The email of the user.
            password (str): The password for the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        # Check if user already exists
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(
                email=email, hashed_password=str(_hash_password(password))
            )

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login credentials by checking email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            # Check password using bcrypt
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except NoResultFound:
            return False

        return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user identified by the given email.

        Args:
            email (str): The email of the user.

        Returns:
            Optional[str]: The newly generated session ID if the user exists,
                 or None if the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
