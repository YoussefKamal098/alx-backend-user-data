#!/usr/bin/env python3
"""
Session-based authentication module using a database (file-based persistence).

This module defines the `SessionDBAuth` class, which provides authentication
mechanisms using session IDs stored in a database (in this case, a file-based
model of `UserSession`). It extends the `SessionExpAuth` class to implement
session creation, user retrieval by session ID, and session destruction.

Classes:
    - SessionDBAuth: Handles session management, including creation,
      validation, and destruction of user sessions, utilizing `UserSession`
      for persistence.

Methods:
    - create_session: Creates a new session ID, stores it with the associated
      user in `UserSession`, and returns the session ID.
    - user_id_for_session_id: Retrieves the user ID for a given session ID,
      verifying session validity and expiration.
    - destroy_session: Destroys the session associated with a session ID from
      the request cookie.
"""

from datetime import datetime, timedelta
import uuid
from typing import Optional

import flask

from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Handles session-based authentication using database storage for sessions.

    This class extends the `SessionExpAuth` class and provides implementations
    for creating sessions, validating user sessions, and destroying sessions
    from storage. It stores session information in the `UserSession` model,
    which is persisted in a file-based database.

    Methods:
        - create_session: Creates a new session for a user and stores it in
          `UserSession`.
        - user_id_for_session_id: Retrieves the user ID for a given session
          ID if the session is valid.
        - destroy_session: Destroys the session associated with the request
          cookie.
    """

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Creates a new session ID for the user and stores the session in the
        `UserSession` model.

        This method generates a new session ID, associates it with the
        provided `user_id`, and saves the session in the database (file-based
        storage). It then returns the session ID for further use.

        Args:
            user_id (str): The user ID to associate with the session. If not
                           provided, defaults to None.

        Returns:
            Optional[str]: The generated session ID, or None if
                session creation fails.
        """
        session_id = str(uuid.uuid4())

        user_session = UserSession(**{
            'user_id': user_id,
            'session_id': session_id
        })

        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        Retrieves the user ID associated with a given session ID.

        This method checks the `UserSession` model for a session matching the
        provided session ID, verifies if it is still valid (based on expiration
        time), and returns the associated user ID. If the session is expired,
        it is removed from storage.

        Args:
            session_id (str): The session ID to search for in the database.

        Returns:
            Optional[str]: The user ID associated with the session, or None if
                           the session is invalid or expired.
        """
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions.first().created_at + time_span

        if datetime.now() > exp_time and self.session_duration > 0:
            sessions.first().remove()
            return None

        return sessions.first().user_id

    def destroy_session(self, request: flask.Request = None) -> bool:
        """
        Destroys the session associated with the request cookie.

        This method retrieves the session ID from the request cookie, searches
        for the corresponding session in the `UserSession` model, and removes
        it from storage if found.

        Args:
            request (flask.Request): The Flask request object containing the
                                     session cookie.

        Returns:
            bool: True if the session was successfully destroyed, False if no
                  session was found or destruction failed.
        """
        session_id = self.session_cookie(request)
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        sessions.first().remove()
        return True
