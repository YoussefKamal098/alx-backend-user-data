#!/usr/bin/env python3
"""
Auth module for handling authentication in the API.

This module contains the base `Auth` class that defines the common interface
and methods for handling authentication in the API. It is intended to
be extended by other authentication models such as
`BasicAuth` or `SessionAuth`, which implement specific authentication
mechanisms.

The `Auth` class provides methods for determining whether authentication
is required, extracting authorization headers, and identifying the
current user, but does not
implement any actual authentication logic. Subclasses must implement
the `current_user` method to provide the necessary functionality.
"""
import os
import re
from typing import List, Optional
from abc import ABC, abstractmethod

import flask

from models.types import UserType


class Auth(ABC):
    """
    Base class for handling authentication requirements in the API.

    The `Auth` class serves as a base for various authentication mechanisms
    in the API. It defines the common interface and basic methods to handle
    authentication logic, which can be extended by subclasses such as
    `BasicAuth` or `SessionAuth` to implement specific authentication methods.

    The class provides methods to:
    - Determine if authentication is required for a given path based on a list
      of excluded paths and wildcard patterns.
    - Extract the `Authorization` header from an incoming request.
    - Retrieve the current user based on the request, though this method
      must be implemented in subclasses.
    """

    @abstractmethod
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

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if the given path requires authentication,
        considering wildcard patterns in excluded_paths.

        This method checks whether a given path requires authentication based
        on whether it matches any of the excluded paths, which can contain
        wildcard patterns (e.g., `/public/*`). If the path matches an excluded
        pattern, authentication is not required; otherwise, authentication
        is required.

        Args:
            path (Optional[str]): The requested path.
            excluded_paths (List[str]): A list of paths that do not require
                authentication. Wildcards (`*`) may be used to match patterns.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if not path or not excluded_paths:
            return True

        # Normalize the path to ensure consistency
        normalized_path = path if path.endswith('/') else path + '/'

        # Check if the normalized path matches any
        # excluded path patterns using regex
        for pattern in excluded_paths:
            # Convert wildcard pattern to a regex pattern
            regex_pattern = re.escape(pattern)
            # Replace '*' with '.*' for regex match
            regex_pattern = regex_pattern.replace(r'\*', '.*')

            # Check if the normalized path matches the regex pattern
            if re.match(regex_pattern + r'/?$', normalized_path):
                # Path matches an excluded pattern, no authentication required
                return False

        # Path doesn't match any excluded pattern, authentication is required
        return True

    def authorization_header(
            self, request: flask.Request = None
    ) -> Optional[str]:
        """
        Retrieve the Authorization header from the request.

        This method checks the request object for the presence of an
        `Authorization` header, which typically contains credentials such as
        a token or user credentials for authentication.

        Args:
            request (Optional[flask.Request]): The request object.

        Returns:
            Optional[str]: The `Authorization` header value
                if present, else None.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def session_cookie(self, request: flask.Request = None) -> Optional[str]:
        """
        Retrieve the session cookie value from the request.

        This method returns the value of the session cookie, which is
        defined by the environment variable SESSION_NAME. If the request
        or the cookie is not present, it returns None.

        Args:
            request (Optional[flask.Request]): The request object.

        Returns:
            str: The value of the session cookie if available, else None.
        """
        if request is None:
            return None

        # Default cookie name is '_my_session_id'
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
