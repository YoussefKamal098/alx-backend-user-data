#!/usr/bin/env python3
"""
A simple script to securely hash passwords and verify them using bcrypt.

This script provides two main functions:
1. `hash_password` - Hashes a password string using bcrypt with
    automatic salting.
2. `is_valid` - Validates a plaintext password against a
    hashed bcrypt password.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a plaintext password using bcrypt with a randomly generated salt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The hashed password as a byte string, which includes the salt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies a plaintext password against a bcrypt hashed password.

    Args:
        hashed_password (bytes): The bcrypt hashed password.
        password (str): The plaintext password to be checked.

    Returns:
        bool: True if the password matches the hashed password,
            False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
