#!/usr/bin/env python3
"""
This module defines the `SessionExpAuth` class, which extends the
functionality of  session-based authentication by
adding session expiration logic. It also includes
an `ExpiringDict` class that stores session data and automatically
removes expired sessions when accessed.

Classes:
    - SessionExpAuth: A subclass of `SessionAuth` that adds session
        expiration functionality.
    - ExpiringDict: A dictionary that automatically deletes expired
        session keys when accessed.

`SessionExpAuth` uses an environment variable `SESSION_DURATION`
to determine the duration of session validity.
Sessions are stored in an instance of `ExpiringDict`,
which tracks the expiration time of each session and deletes
expired sessions when they are accessed.
It overrides the `create_session`, `user_id_for_session_id`,
and other session management methods from `SessionAuth`.

`ExpiringDict` is a specialized dictionary that:
    - Stores sessions with a `created_at` timestamp.
    - Deletes entries that have expired based on the provided expiration time.
    - Prevents iteration and size retrieval.
"""

import os
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth and
    adds session expiration logic.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth class.

        Sets the session_duration attribute from the environment
        variable `SESSION_DURATION`. If not set or if it can't be
        cast to an integer, defaults to 0.
        """
        super().__init__()

        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

        self.user_id_by_session_id = ExpiringDict(self.session_duration)

    def create_session(self, user_id=None):
        """
        Create a session ID with an expiration time.

        Args:
            user_id (str): The user ID for whom the session is being created.

        Returns:
            str: The session ID created, or None if it can't be created.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Add session to the dictionary with expiration
        self.user_id_by_session_id[session_id] = \
            {'user_id': user_id, "created_at": datetime.now()}

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve user ID for the given session ID, considering expiration.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID if valid, or None if the session has
                expired or doesn't exist.
        """
        if session_id is None:
            return None

        session = self.user_id_by_session_id[session_id]
        if not session:
            return None

        return session['user_id']


class ExpiringDict:
    """
    A dictionary that automatically deletes expired keys when accessed.
    This does not inherit from dict but mimics its behavior.
    """

    def __init__(self, expiration_time):
        self.expiration_time = expiration_time
        self._data = {}

    def __getitem__(self, key):
        """
        Retrieve an item by key, but remove it if it's expired.
        """
        if key not in self._data:
            # raise KeyError(f"{key} not found in the dictionary.")
            return None

        value = self._data[key]
        created_at = value.get("created_at")

        if not created_at:
            # raise KeyError(f"{key} does not have a creation timestamp.")
            return None

        # Check if session is expired
        if not self._is_valid(key):
            # Session expired, delete the key and raise an exception
            self._expire_key(key)
            # raise KeyError(f"{key} has expired and been removed.")
            return None

        return value['value']

    def _expire_key(self, key):
        """
        Delete a session key when it expires.
        """
        if key in self._data:
            del self._data[key]

    def __setitem__(self, key, value):
        """
        Store an item in the dictionary with an expiration timestamp.
        """
        self._data[key] = {"value": value, "created_at": datetime.now()}

    def __delitem__(self, key):
        """
        Delete an item from the dictionary.
        """
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"{key} not found in the dictionary.")

    def __contains__(self, key):
        """
        Check if a key exists in the dictionary.
        """
        return key in self._data

    def __iter__(self):
        """
        Prevent iteration over the dictionary keys.
        """
        raise TypeError("This dictionary is not iterable.")

    def __len__(self):
        """
        Prevent retrieval of the size of the dictionary.
        """
        raise TypeError("Size of this dictionary cannot be retrieved.")

    def __str__(self):
        """
        Return a string representation of the dictionary
        showing key-value pairs where values are not expired.
        """
        valid_items = {
            key: value['value']
            for key, value in
            self._data.items() if self._is_valid(key)
        }
        return str(valid_items)

    def __repr__(self):
        """
        Return a more formal string representation of the
        dictionary showing key-value pairs where values are not expired.
        """
        valid_items = {
            key: value['value']
            for key, value in
            self._data.items() if self._is_valid(key)
        }
        return f"ExpiringDict({valid_items})"

    def _is_valid(self, key):
        """
        Helper method to check if a key's session is valid (not expired).
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
