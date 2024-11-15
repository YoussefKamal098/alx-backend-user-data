#!/usr/bin/env python3
"""
SessionAuth Module

This module defines the SessionAuth class, which is a subclass
of the Auth class. This class serves as a placeholder for future logic and
functionality related to session-based authentication.

Currently, it inherits from Auth without any additional logic.
"""
import uuid
from typing import Optional

import flask

from api.v1.auth.auth import Auth
from models.user import User
from models.types import UserType


class SessionAuth(Auth):
    """
    SessionAuth class inheriting from Auth, placeholder for future logic.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Create a new session ID for the given user ID and store it
        in the user_id_by_session_id dictionary.

        Args:
            user_id (str, optional): The user ID to create a session for.
                Defaults to None.

        Returns:
            str: The session ID if user_id is valid, else None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def destroy_session(self, request: flask.Request = None) -> bool:
        """
        Destroy a user's session by removing the session ID.

        Args:
            request (flask.Request): The request object.

        Returns:
            bool: True if the session was successfully destroyed, otherwise False.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """Retrieve the User ID based on the given session ID."""
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(
            self, request: flask.Request = None
    ) -> Optional[UserType]:
        """
        Retrieve the current user based on the request.

        This method is intended to be overridden in subclasses to extract
        the user from the request based on the authentication mechanism.
        By default, it returns None, indicating no authenticated user.

        Args:
            request (Optional[flask.Request]): The request object.

        Returns:
            Optional[UserType]: The current authenticated user if
                available, else None.
        """
        # Retrieve the session ID from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Retrieve the user ID from the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve the user instance from the database using User.get()
        return User.get(user_id)  # Assuming User.get() retrieves a user by ID
