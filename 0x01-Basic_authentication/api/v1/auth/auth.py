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
implement any actual authentication logic. Subclasses should extend
this class to provide the necessary functionality.
"""

import re
from typing import List, Optional
from models.types import UserType


class Auth:
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
      does not implement user retrieval logic and is intended to be
      overridden in subclasses.

    This class does not contain the actual authentication logic.
    It is intended to be extended and customized to provide the
    necessary authentication functionality.
    """

    def require_auth(self, path, excluded_paths):
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

        """
        Check if the normalized path matches any
        excluded path patterns using regex
        """
        for pattern in excluded_paths:
            # Convert wildcard pattern to a regex pattern

            # Escape special characters in the pattern
            regex_pattern = re.escape(pattern)
            # Replace '*' with '.*' for regex match
            regex_pattern = regex_pattern.replace(r'\*', '.*')

            """Check if the normalized path matches the regex pattern
            and The '$' ensures the end of the string"""
            if re.match(regex_pattern + r'/?$', normalized_path):
                # Path matches an excluded pattern, no authentication required
                return False

        # Path doesn't match any excluded pattern, authentication is required
        return True

    def authorization_header(self, request=None) -> Optional[str]:
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

    def current_user(self, _request=None) -> Optional[UserType]:
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
        return None
