#!/usr/bin/env python3
""" User module
"""
import hashlib
from typing import List, Dict, Any, Optional

from models.base import Base


class User(Base):
    """ User class """

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """ Initialize a User instance """
        super().__init__(*args, **kwargs)

        self.email: Optional[str] = kwargs.get('email')
        self._password: Optional[str] = kwargs.get('_password')
        self.first_name: Optional[str] = kwargs.get('first_name')
        self.last_name: Optional[str] = kwargs.get('last_name')

    @property
    def password(self) -> Optional[str]:
        """ Getter for the password """
        return self._password

    @password.setter
    def password(self, pwd: Optional[str]):
        """ Setter for a new password: encrypt in SHA256 """
        if not isinstance(pwd, str) or not pwd:
            self._password = None
        else:
            self._password = self._encrypt_password(pwd)

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password """
        if not isinstance(pwd, str) or not pwd or not self.password:
            return False
        return self._encrypt_password(pwd) == self.password

    def display_name(self) -> str:
        """ Display the full name based on email, first name, and last name """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email or ""

    @staticmethod
    def _encrypt_password(pwd: str) -> str:
        """ Encrypt the password using SHA256 """
        return hashlib.sha256(pwd.encode()).hexdigest().lower()
