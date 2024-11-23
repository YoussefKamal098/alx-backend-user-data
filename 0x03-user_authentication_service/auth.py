#!/usr/bin/env python3
"""
Password hashing module using bcrypt.

This module provides functionality for securely hashing passwords using
the bcrypt algorithm. It includes a method for hashing a password with
a salt, which ensures that even if two users have the same password,
their hashes will be different.

Additionally, the `Auth` class is implemented to handle user registration
by checking if a user exists in the database and securely hashing their
password before storing it.

Functions:
    _hash_password(password: str) -> bytes:
        Hashes the given password using bcrypt and returns the hash as a
        binary string.

Classes:
    Auth:
        A class responsible for user registration and authentication.
        It checks if a user exists and stores the hashed password.

"""
import bcrypt

from sqlalchemy.orm.exc import NoResultFound
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
                email=email, hashed_password=_hash_password(password)
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
