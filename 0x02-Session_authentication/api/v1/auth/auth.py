#!/usr/bin/env python3
"""
Authentication Module

This module defines the `AuthInterface` and `Auth` classes to handle
authentication mechanisms within the API. The `AuthInterface` outlines
the required methods for implementing authentication systems such as
BasicAuth, SessionAuth, or custom authentication mechanisms. The `Auth`
class serves as a base class for these mechanisms and provides common
authentication logic, which can be extended by subclasses.

Classes:
    - AuthInterface: An abstract class that defines the methods to be
      implemented by authentication classes.
    - Auth: A base class for handling common authentication logic and
      requirements for API paths.

Methods in `AuthInterface`:
    - current_user: Retrieves the current authenticated user from the request.
    - require_auth: Determines if the requested path requires authentication.
    - authorization_header:Extracts the Authorization header from the request.
    - session_cookie: Retrieves the session cookie from the request.

Methods in `Auth`:
    - current_user: Retrieves the current authenticated user, to be
      implemented by subclasses.
    - require_auth: Determines if a path requires authentication,
      considering excluded paths and wildcard patterns.
    - authorization_header: Retrieves the `Authorization` header from the
      request.
    - session_cookie: Retrieves the session cookie from the request.
"""
import re
from abc import ABC, abstractmethod
from typing import List, Optional

import flask

from models.types import UserType
from config import config
from utils import override


class AuthInterface(ABC):
    """
    Interface for handling authentication in the API.

    This interface defines the methods that must be implemented by any
    authentication class, such as BasicAuth, SessionAuth,
    or custom auth mechanisms.
    """

    @abstractmethod
    def current_user(
            self, _request: flask.Request = None
    ) -> Optional[UserType]:
        """
        Retrieve the current authenticated user based on the request.

        Args:
            _request (Optional[flask.Request]): The request object.

        Returns:
            Optional[UserType]: The current authenticated user if
                available, else None.
        """
        pass

    @abstractmethod
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if the given path requires authentication.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]): List of paths that do not
                require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        pass

    @abstractmethod
    def authorization_header(
            self, request: flask.Request = None
    ) -> Optional[str]:
        """
        Retrieve the Authorization header from the request.

        Args:
            request (Optional[flask.Request]): The request object.

        Returns:
            Optional[str]: The Authorization header value if present,
                else None.
        """
        pass

    @abstractmethod
    def session_cookie(self, request: flask.Request = None) -> Optional[str]:
        """
        Retrieve the session cookie value from the request.

        Args:
            request (Optional[flask.Request]): The request object that
                contains the cookies.

        Returns:
            Optional[str]: The value of the session cookie if it exists,
                otherwise None.
        """
        pass


class Auth(AuthInterface):
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

    @override
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

        This method attempts to retrieve the value of the session cookie from
        the request. The name of the session cookie is defined by the
        environment variable `SESSION_NAME`, which is typically set in
        the Flask app's configuration. If the request is not provided or
        if the session cookie is not found, the method will return None.

        Args:
           request (Optional[flask.Request]):
                The request object that contains the cookies.
                If not provided, the method will attempt to
                retrieve the cookie from the current request.

        Returns:
           Optional[str]: The value of the session cookie if it exists,
                otherwise None.
       """
        if request is None:
            return None

        return request.cookies.get(config.SESSION_NAME)
