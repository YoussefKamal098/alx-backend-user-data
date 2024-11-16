#!/usr/bin/env python3
"""
Auth Factory Module

This module defines an abstract factory and its concrete implementations
for creating different types of authentication instances. The factories
ensure that the correct authentication mechanism (e.g., BasicAuth,
SessionAuth, SessionExpAuth) is instantiated based on the
desired authentication method.

Classes:
    - AuthFactory: Abstract base class for creating authentication instances.
    - BasicAuthFactory: Factory for creating BasicAuth instance.
    - SessionAuthFactory: Factory for creating SessionAuth instance.
    - SessionExpAuthFactory: Factory for creating SessionExpAuth instance.
"""
from abc import ABC, abstractmethod
from api.v1.auth.auth import AuthInterface
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


class AuthFactory(ABC):
    """Abstract factory for creating Auth instances."""

    @abstractmethod
    def create_auth(self) -> AuthInterface:
        """Method to create and return an authentication instance."""
        pass


class BasicAuthFactory(AuthFactory):
    """Factory for creating BasicAuth instance."""

    def create_auth(self) -> AuthInterface:
        return BasicAuth()


class SessionAuthFactory(AuthFactory):
    """Factory for creating SessionAuth instance."""

    def create_auth(self) -> AuthInterface:
        return SessionAuth()


class SessionExpAuthFactory(AuthFactory):
    """Factory for creating SessionExpAuth instance."""

    def create_auth(self) -> AuthInterface:
        """
        Returns an instance of SessionExpAuth, which implements
        session expiration logic in addition to standard
        session authentication.
        """
        return SessionExpAuth()
