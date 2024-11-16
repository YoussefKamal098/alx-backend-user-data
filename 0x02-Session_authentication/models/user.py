#!/usr/bin/env python3
"""
User class for managing user data
"""
from typing import List, Dict, Any, Optional

from models.base import Base
from utils import encrypt_password


class User(Base):
    """
    Represents a user with attributes like email, password, and full name.
    """

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """Initializes a User instance with optional attributes."""
        super().__init__(*args, **kwargs)

        self.email: Optional[str] = kwargs.get('email')
        self._password: Optional[str] = kwargs.get('_password')
        self.first_name: Optional[str] = kwargs.get('first_name')
        self.last_name: Optional[str] = kwargs.get('last_name')

    @property
    def password(self) -> Optional[str]:
        """Returns the user's encrypted password."""
        return self._password

    @password.setter
    def password(self, pwd: Optional[str]):
        """Encrypts and sets a new password."""
        if not isinstance(pwd, str) or not pwd:
            self._password = None
        else:
            self._password = encrypt_password(pwd)

    def is_valid_password(self, pwd: str) -> bool:
        """Checks if the provided password matches the stored password."""
        if not isinstance(pwd, str) or not pwd or not self.password:
            return False
        return encrypt_password(pwd) == self.password

    def display_name(self) -> str:
        """Generates a display name based on the user's attributes."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email or ""
