#!/usr/bin/env python3
"""Auth module for the API."""

import re
from typing import List, Optional
from models.types import UserType


class Auth:
    """Auth class for handling authentication requirements."""

    def require_auth(self, path, excluded_paths):
        """
        Determine if the given path requires authentication,
        considering wildcard patterns in excluded_paths.

        Args:
            path (Optional[str]): The requested path.
            excluded_paths (List[str]): Paths that do not require
                authentication (with optional wildcards).

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
        """Retrieve the Authorization header from the request.

        Args:
            request (Optional[flask.Request]): The request object.

        Returns:
            Optional[str]: The Authorization header if present, else None.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, _request=None) -> Optional[UserType]:
        """Retrieve the current user based on the request.

        Args:
            _request (Optional[flask.Request]): The request object.

        Returns:
            Optional[UserType]: The current user if authenticated, else None.
        """
        return None
