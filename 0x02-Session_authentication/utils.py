#!/usr/bin/env python3
"""
utils Module

This module provides utility functions and classes that are commonly
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

Classes:
    ExpiringDict:
        A dictionary that automatically deletes expired keys when accessed.
        Mimics the behavior of a regular dictionary but adds expiration
        functionality to automatically remove expired entries.

The utilities aim to ensure code consistency, security,
and better error handling.
"""
from datetime import datetime, timedelta
from typing import Any, Optional
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


class ExpiringDict:
    """
    A dictionary that automatically deletes expired keys when accessed.
    This does not inherit from dict but mimics its behavior.

    Attributes:
        expiration_time (int): The expiration time for keys in seconds.
            If set to 0, keys do not expire.
        _data (dict): A dictionary storing the actual data with timestamps.
    """

    def __init__(self, expiration_time: int = 0) -> None:
        """
        Initialize the ExpiringDict with an expiration time.
        If expiration_time is 0, no expiration is applied.

        Args:
            expiration_time (int): The expiration time for keys in seconds.
                Defaults to 0 (no expiration).
        """
        self.expiration_time = expiration_time
        self._data = {}

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Retrieve an item by key, removing it if expired. Returns a default
        value if the key is not found or is expired.

        Args:
            key (Any): The key of the item to retrieve.
            default (Optional[Any], optional): Default value if the key is not
                found or expired. Defaults to None.

        Returns:
            Optional[Any]: The value associated with the key,
                or the default value if expired or not found.
        """
        if key in self._data:
            return self[key]
        return default

    def __getitem__(self, key: Any) -> Optional[Any]:
        """
        Retrieve an item by key, but remove it if expired.
        If expired, the key is removed and None is returned.

        Args:
            key (Any): The key of the item to retrieve.

        Returns:
            Optional[Any]: The value associated with the key,
                or None if expired or not found.
        """
        if key not in self._data:
            return None

        value = self._data[key]
        created_at = value.get("created_at")

        if not created_at:
            self.expire_key(key)
            return None

        if not self._is_valid(key):
            self.expire_key(key)
            return None

        return value['value']

    def expire_key(self, key: Any) -> None:
        """
        Delete a key from the dictionary when it expires.

        Args:
            key (Any): The key to expire.
        """
        if key in self._data:
            del self._data[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Store an item in the dictionary with a creation timestamp.

        Args:
            key (Any): The key to store.
            value (Any): The value associated with the key to store.
        """
        self._data[key] = {"value": value, "created_at": datetime.now()}

    def __delitem__(self, key: Any) -> None:
        """
        Delete an item from the dictionary by key.

        Args:
            key (Any): The key to delete.

        Raises:
            KeyError: If the key is not found in the dictionary.
        """
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"{key} not found in the dictionary.")

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key exists in the dictionary.

        Args:
            key (Any): The key to check for existence.

        Returns:
            bool: True if the key exists in the dictionary, False otherwise.
        """
        return key in self._data

    def __iter__(self) -> None:
        """
        Prevent iteration over the dictionary.

        Raises:
            TypeError: This dictionary is not iterable.
        """
        raise TypeError("This dictionary is not iterable.")

    def __len__(self) -> None:
        """
        Prevent retrieval of the size of the dictionary.

        Raises:
            TypeError: Size of this dictionary cannot be retrieved.
        """
        raise TypeError("Size of this dictionary cannot be retrieved.")

    def __str__(self) -> str:
        """
        Return a string representation of the dictionary showing
        only key-value pairs where values are not expired.

        Returns:
            str: A string representation of the
                valid (non-expired) key-value pairs.
        """
        valid_items = {
            key: value['value']
            for key, value in self._data.items() if self._is_valid(key)
        }
        return str(valid_items)

    def __repr__(self) -> str:
        """
        Return a more formal string representation of
        the dictionary showing valid (non-expired) key-value pairs.

        Returns:
            str: A formal string representation of
                the valid (non-expired) key-value pairs.
        """
        valid_items = {
            key: value['value']
            for key, value in self._data.items() if self._is_valid(key)
        }
        return f"ExpiringDict({valid_items})"

    def _is_valid(self, key: Any) -> bool:
        """
        Helper method to check if a key's session is valid (not expired).

        Args:
            key (Any): The key to check.

        Returns:
            bool: True if the key is valid (not expired), False otherwise.
        """
        if self.expiration_time <= 0:
            return True

        if key not in self._data:
            return False

        value = self._data[key]
        created_at = value.get("created_at")

        if not created_at:
            return False

        expiration_time = created_at + timedelta(seconds=self.expiration_time)
        return expiration_time >= datetime.now()
