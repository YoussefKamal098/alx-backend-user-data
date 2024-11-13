#!/usr/bin/env python3
"""
BasicAuth module

This module provides an implementation of basic authentication
for API requests.

It extracts and decodes the `Authorization` header,
retrieves user credentials, and verifies user authenticity
using stored user information.

The `BasicAuth` class inherits from the `Auth` class and includes methods for
extracting, decoding, and validating user credentials from base64-encoded
authorization headers.

"""

import re
import base64
# import binascii
from typing import Tuple, Optional
from api.v1.auth.auth import Auth
from models.user import User
from models.types import UserType


class BasicAuth(Auth):
    """
    BasicAuth class handles the extraction and validation of user credentials
    for API requests using Basic Authentication. It provides methods to
    extract and decode base64-encoded authorization headers,
    extract user credentials, and verify the user's authenticity.

    Inherits from the `Auth` class and provides additional functionality
    specific to basic authentication schemes.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> Optional[str]:
        """
        Extract the base64-encoded authorization string from the
        Authorization header.

        Args:
            authorization_header (str): The value of the Authorization header.

        Returns:
            Optional[str]: The base64-encoded authorization string if
                valid, otherwise None.
        """
        if not isinstance(authorization_header, str):
            return None

        """
        Regular expression to match "Basic " followed by a valid Base64 string
        """
        match = re.match(
            r"^Basic (?P<base64String>[A-Za-z0-9+/=]+)$",
            authorization_header
        )

        if match:
            return match.group('base64String')

        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> Optional[str]:
        """
        Decode the base64-encoded authorization header into
        a human-readable string.

        Args:
            base64_authorization_header (str):
                The base64-encoded authorization string.

        Returns:
            Optional[str]: The decoded string if successful, otherwise None.
        """
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract the username and password from the
        decoded base64 authorization string.

        Args:
            decoded_base64_authorization_header (str): The decoded
                authorization string in the format "username:password".

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the
                username and password if valid, otherwise (None, None).
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        # Regular expression with named capture groups
        match = re.match(
            r"^(?P<username>[^:]+):(?P<password>.*)$",
            decoded_base64_authorization_header
        )

        if match:
            return match.group('username'), match.group('password')

        # If not a valid format, return None, None
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> Optional[UserType]:
        """
        Retrieve the user object based on the provided email and password.

        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.

        Returns:
            Optional[UserType]: The User object if credentials
                are valid, otherwise None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]  # Assuming we get only one user
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> Optional[UserType]:
        """
        Retrieve the current user based on
        the `Authorization` header from the request.

        Args:
            request: The HTTP request object containing headers.

        Returns:
            Optional[UserType]: The User object if
                authenticated, otherwise None.
        """
        if not request:
            return None

        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None

        base64_authorization_header = \
            self.extract_base64_authorization_header(authorization_header)
        if not base64_authorization_header:
            return None

        decoded_base64_authorization_header = \
            self.decode_base64_authorization_header(
                base64_authorization_header)

        if not decoded_base64_authorization_header:
            return None

        user_email, user_pwd = \
            self.extract_user_credentials(decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
