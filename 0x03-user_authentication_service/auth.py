#!/usr/bin/env python3
"""
Password hashing module using bcrypt.

This module provides functionality for securely hashing passwords using
the bcrypt algorithm. It includes a method for hashing a password with
a salt, which ensures that even if two users have the same password,
their hashes will be different.
"""
import bcrypt


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
