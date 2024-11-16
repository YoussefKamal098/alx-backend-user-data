#!/usr/bin/env python3
"""
Session Authentication Module

This module defines the `SessionAuthInterface` and `SessionAuth` classes for
session-based authentication. The `SessionAuthInterface` outlines the
required methods for session authentication, and `SessionAuth` implements
these methods for managing user sessions using in-memory data storage.

Classes:
    - SessionAuthInterface: An abstract base class that defines the
      interface for session authentication.
    - SessionAuth: A class that implements the session authentication
      methods, using in-memory storage for session management.

Methods in `SessionAuthInterface`:
    - create_session: Creates a session for a user.
    - destroy_session: Destroys the session for a user based on the request.
    - user_id_for_session_id: Retrieves the user ID based on the session ID.
    - current_user: Retrieves the current user based on the session.

Methods in `SessionAuth`:
    - create_session: Creates a session for the user and stores it in memory.
    - destroy_session: Destroys the session using the provided request.
    - user_id_for_session_id: Retrieves the user ID for the given session ID.
    - current_user: Retrieves the current authenticated user based on the
      session ID.
"""

import uuid
from abc import ABC, abstractmethod
from typing import Optional

import flask

from api.v1.auth.auth import AuthInterface, Auth
from models.user import User
from models.types import UserType


class SessionAuthInterface(AuthInterface, ABC):
    """
    Interface for Session Authentication classes.

    This abstract class defines the methods that must be implemented
    by any session-based authentication class, such as
    creating sessions, destroying sessions,
    and retrieving user information based on sessions.
    """

    @abstractmethod
    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Create a new session for the given user ID.

        Args:
            user_id (str, optional): The user ID to create a session for.

        Returns:
            Optional[str]: The session ID if successful, None otherwise.
        """
        pass

    @abstractmethod
    def destroy_session(self, request: flask.Request = None) -> bool:
        """
        Destroy a session for the user based on the provided request.

        Args:
            request (flask.Request): The request object.

        Returns:
            bool: True if session is successfully destroyed, otherwise False.
        """
        pass

    @abstractmethod
    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        Retrieve the user ID associated with the given session ID.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            Optional[str]: The user ID if found, None otherwise.
        """
        pass

    @abstractmethod
    def current_user(
            self, request: flask.Request = None
    ) -> Optional[UserType]:
        """
        Retrieve the current authenticated user based on the session.

        Args:
            request (flask.Request, optional): The request object.

        Returns:
            Optional[UserType]: The current authenticated user if available,
                None otherwise.
        """
        pass


class SessionAuth(Auth, SessionAuthInterface):
    """
     SessionAuth class for handling session-based authentication.

     This class provides functionality to create and manage user sessions
     using session IDs stored in memory. It is a subclass of the Auth class
     and offers methods for creating, destroying, and retrieving sessions.

     Currently, it operates using a dictionary to map session IDs to user IDs
     and provides methods to interact with these sessions, such as creating a
     new session for a user, destroying a session, and retrieving the user ID
     associated with a session.

     All session data is stored in memory, meaning that all sessions will be
     lost when the application restarts.

     Attributes:
         user_id_by_session_id (dict): A dictionary mapping session IDs
         to user IDs.

     Methods:
         create_session(user_id: str) -> Optional[str]:
             Creates a new session for the given user ID and
             returns the session ID.

         destroy_session(request: flask.Request) -> bool:
             Destroys the session for the user associated with the
             provided request.

         user_id_for_session_id(session_id: str) -> Optional[str]:
             Retrieves the user ID associated with the given session ID.

         current_user(request: flask.Request) -> Optional[UserType]:
             Retrieves the current authenticated user based on the request,
             using the session ID.
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
            bool: True if the session was successfully destroyed,
                otherwise False.
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
