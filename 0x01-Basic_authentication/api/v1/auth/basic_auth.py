#!/usr/bin/env python3
"""
BasicAuth module
"""
import re
import base64
import binascii
from typing import Tuple, Optional
from api.v1.auth.auth import Auth
from models.user import User
from models.types import UserType


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        if not isinstance(authorization_header, str):
            return None

        # Regular expression to match "Basic " followed by a valid Base64 string
        match = re.match(r"^Basic (?P<base64String>[A-Za-z0-9+/=]+)$", authorization_header)
        if match:
            return match.group('base64String')

        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header).decode("utf-8")
            return decoded
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        # Regular expression with named capture groups
        match = re.match(r"^(?P<username>[^:]+):(?P<password>.*)$", decoded_base64_authorization_header)
        if match:
            return match.group('username'), match.group('password')

        # If not a valid format, return None, None
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[UserType]:
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})  # Assuming search method filters by email
        if not users:
            return None

        user = users[0]  # Assuming we get only one user
        if not user.is_valid_password(user_pwd):  # Assuming method to validate password
            return None

        return user

    def current_user(self, request=None) -> Optional[UserType]:
        if not request:
            return None

        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        if not base64_authorization_header:
            return None

        decoded_base64_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        if not decoded_base64_authorization_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
