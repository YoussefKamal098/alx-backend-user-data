#!/usr/bin/env python3
"""
Module for managing authentication factories using the Abstract Factory
pattern. Provides a default implementation to return and manage different
authentication types. Supports adding/removing custom authentication
factories dynamically.
"""

from abc import ABC, abstractmethod

from api.v1.auth.auth_factory import (
    BasicAuthFactory,
    SessionAuthFactory,
    SessionExpAuthFactory,
    SessionDBAuthFactory
)
from api.v1.auth.auth_factory import AuthFactory


class AuthFactoryProvider(ABC):
    """Abstract Factory Provider for creating authentication factories."""

    @abstractmethod
    def get_factory(self, auth_type: str) -> AuthFactory:
        """Return the corresponding AuthFactory for the given auth_type."""
        pass

    @abstractmethod
    def add_factory(self, auth_type: str, factory_class: AuthFactory) -> None:
        """Dynamically add a new authentication factory to the provider."""
        pass

    @abstractmethod
    def remove_factory(self, auth_type: str) -> None:
        """Dynamically remove an authentication factory from the provider."""
        pass


class DefaultAuthFactoryProvider(AuthFactoryProvider):
    """
    Default provider for creating the appropriate AuthFactory based
    on AUTH_TYPE.
    """

    FACTORY_MAP = {
        'basic_auth': BasicAuthFactory,
        'session_auth': SessionAuthFactory,
        'session_exp_auth': SessionExpAuthFactory,
        'session_db_auth': SessionDBAuthFactory,
    }

    def get_factory(self, auth_type: str) -> AuthFactory:
        """Return the corresponding AuthFactory for the given auth_type."""
        try:
            factory = self.FACTORY_MAP[auth_type]
        except KeyError:
            raise ValueError(f"Unsupported AUTH_TYPE: {auth_type}")
        return factory()

    def add_factory(self, auth_type: str, factory_class: AuthFactory) -> None:
        """Add a new authentication factory."""
        if auth_type in self.FACTORY_MAP:
            raise ValueError(f"AUTH_TYPE '{auth_type}' already exists.")
        self.FACTORY_MAP[auth_type] = factory_class

    def remove_factory(self, auth_type: str) -> None:
        """Remove an authentication factory."""
        if auth_type not in self.FACTORY_MAP:
            raise ValueError(f"AUTH_TYPE '{auth_type}' does not exist.")
        del self.FACTORY_MAP[auth_type]
