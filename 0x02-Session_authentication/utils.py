#!/usr/bin/env python3
"""
utils Module

This module provides utility functions and decorators that are commonly
used across different parts of the project. It includes the following:

Functions:
    override:
        Decorator to enforce that a method must be overridden
        in a subclass.
    encrypt_sha256:
        Encrypts a string using the SHA256 hashing algorithm.
    parse_int_str:
        Parses a string into an integer, returning a default value
        if parsing fails.

The utilities aim to ensure code consistency, security,
and better error handling.
"""

import functools
import hashlib


def override(method):
    """
    Decorator to enforce that a method must be overridden in a subclass.

    This decorator ensures that any subclass of a base class using
    the `@override` decorator must override the decorated method.
    If the subclass does not provide its implementation, an error is raised.

    Args:
        method (function): The method to be decorated.

    Returns:
        function: The wrapper function that enforces the override.

    Raises:
        NotImplementedError: If the method is not overridden in the subclass.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Check if the method exists in the subclass
        if method.__name__ in self.__class__.__dict__:
            # Ensure that the method is not the base class method
            if self.__class__.__dict__[method.__name__] is method:
                raise NotImplementedError(
                    f"The method `{method.__name__}` "
                    f"must be overridden in the subclass "
                    f"`{self.__class__.__name__}`."
                )
        else:
            # If the method is not implemented in the subclass, raise an error
            raise NotImplementedError(
                f"The method `{method.__name__}` "
                f"must be overridden in the subclass "
                f"`{self.__class__.__name__}`."
            )
        return method(self, *args, **kwargs)

    return wrapper


def encrypt_sha256(value: str) -> str:
    """
    Encrypt the input string using SHA256.

    Args:
        value (str): The string to be encrypted.

    Returns:
        str: The SHA256 hash of the input string in
            lowercase hexadecimal format.
    """
    if not isinstance(value, str):
        raise TypeError("Input to encrypt_sha256 must be a string.")
    return hashlib.sha256(value.encode()).hexdigest().lower()


def parse_int_str(value: str, default: int = 0) -> int:
    """
    Parse a string into an integer, or return a default value if
    parsing fails.

    Args:
        value (str): The string value to parse.
        default (int): The default value to return if parsing fails.

    Returns:
        int: Parsed integer value or the default value.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
