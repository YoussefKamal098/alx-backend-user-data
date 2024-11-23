#!/usr/bin/env python3
"""
Password hashing module using bcrypt.

This module provides functionality for securely hashing passwords using
the bcrypt algorithm. It includes a method for hashing a password with
a salt, which ensures that even if two users have the same password,
their hashes will be different.
"""
import bcrypt

def _hash_password(password: str) -> str:
    """
   Hashes the given password using bcrypt and returns the
   hash in hexadecimal format.

   This method takes a plain text password, generates a random salt,
   and applies the bcrypt algorithm to hash the password.
   The result is returned as a hexadecimal string.

   Args:
       password (str): The plain text password to be hashed.

   Returns:
       str: The hashed password in hexadecimal format,
            including the salt and the bcrypt hash.
   """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).hex()
