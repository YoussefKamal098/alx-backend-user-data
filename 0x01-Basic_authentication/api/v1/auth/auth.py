#!/usr/bin/env python3
""" Auth module for the API"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """

        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        normalized_path = path if path.endswith('/') else path + '/'

        return normalized_path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None
