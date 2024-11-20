#!/usr/bin/env python3
"""
This module Defines the `UserSession` class for persisting
user-session associations in a persistent storage.
Tracks `user_id` and `session_id` for session management.
"""
from models.base import Base


class UserSession(Base):
    """
    Represents a user session with `user_id` and `session_id` attributes.
    Used to persist user sessions in the filesystem storage
    instead of in memory.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a new UserSession instance with user_id and session_id.
        """
        # Initialize user_id and session_id based on provided arguments
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

        # Optionally, pass *args and **kwargs to the parent class if needed
        super().__init__(*args, **kwargs)
