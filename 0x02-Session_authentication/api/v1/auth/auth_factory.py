#!/usr/bin/env python3
"""
Abstract factory pattern for creating Auth instances.
Defines factories for creating BasicAuth and SessionAuth instances.
Each factory implements the create_auth method to
instantiate corresponding Auth classes.
"""
from abc import ABC, abstractmethod
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


class AuthFactory(ABC):
    """Abstract factory for creating Auth instances."""

    @abstractmethod
    def create_auth(self) -> Auth:
        """Method to create and return an authentication instance."""
        pass


class BasicAuthFactory(AuthFactory):
    """Factory for creating BasicAuth instance."""

    def create_auth(self) -> Auth:
        return BasicAuth()


class SessionAuthFactory(AuthFactory):
    """Factory for creating SessionAuth instance."""

    def create_auth(self) -> Auth:
        return SessionAuth()
