#!/usr/bin/env python3
"""
SessionAuth Module

This module defines the SessionAuth class, which is a subclass
of the Auth class. This class serves as a placeholder for future logic and
functionality related to session-based authentication.

Currently, it inherits from Auth without any additional logic.
"""
from typing import Optional

import flask

from api.v1.auth.auth import Auth
from models.types import UserType


class SessionAuth(Auth):
    """
    SessionAuth class inheriting from Auth, placeholder for future logic.
    """
    def current_user(
            self, _request: flask.Request = None
    ) -> Optional[UserType]:
        """
        Retrieve the current user based on the request.

        This method is intended to be overridden in subclasses to extract
        the user from the request based on the authentication mechanism.
        By default, it returns None, indicating no authenticated user.

        Args:
            _request (Optional[flask.Request]): The request object.

        Returns:
            Optional[UserType]: The current authenticated user if
                available, else None.
        """
        pass
