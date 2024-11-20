#!/usr/bin/env python3
"""
This module defines the `SessionExpAuth` class, which extends the
functionality of  session-based authentication by
adding session expiration logic.

Classes:
    - SessionExpAuth: A subclass of `SessionAuth` that adds session
        expiration functionality.

`SessionExpAuth` uses an environment variable `SESSION_DURATION`
to determine the duration of session validity.
Sessions are stored in an instance of `ExpiringDict`,
which tracks the expiration time of each session and deletes
expired sessions when they are accessed.
It overrides the `create_session`, `user_id_for_session_id`,
and other session management methods from `SessionAuth`.
"""
from datetime import datetime
from typing import Optional

from api.v1.auth.session_auth import SessionAuth
from config import config
from utils import ExpiringDict


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
        self.session_duration = config.SESSION_DURATION
        self.user_id_by_session_id = ExpiringDict(self.session_duration)

    def create_session(self, user_id: str = None) -> Optional[str]:
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

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
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

        if not session.get("created_at"):
            self.user_id_by_session_id.expire_key(session_id)
            return None

        return session.get('user_id')
