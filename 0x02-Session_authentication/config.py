#!/usr/bin/env python3
"""
Config Module

This module provides a singleton configuration class for managing
environment variables in a Python application.
The `Config` class uses the `@dataclass` decorator for
immutability and simplicity while allowing dynamic default
values through the `field(default_factory=...)` mechanism.

Features:
- Singleton pattern ensures a single instance of the configuration
    is used throughout the application.
- Environment variables are dynamically fetched for configuration values,
    with sensible defaults provided.
- Includes utility integration (e.g., `parse_int_str`) for
    robust parsing of environment variables.

Classes:
    Config:
        A frozen dataclass implementing a singleton pattern to manage
        application-wide configuration settings.

Usage:
    # Access the singleton instance
    config = Config.get_instance()
    print(config.API_HOST)  # Outputs the API host configuration

Raises:
    TypeError: If the `Config` class is instantiated directly
        instead of using the `get_instance` method.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from utils import parse_int_str

@dataclass(frozen=True)
class Config:
    """Singleton Configuration class for managing environment variables."""

    # Configuration fields
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: str = os.getenv("API_PORT", "5000")
    SESSION_NAME: str = os.getenv("SESSION_NAME", "_my_session_id")
    SESSION_DURATION: int = parse_int_str(os.getenv("SESSION_DURATION", "0"))
    AUTH_TYPE: str =  os.getenv('AUTH_TYPE', 'basic_auth')

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            raise TypeError(
                "Config class is a singleton."
                "Use `Config.get_instance()` to access the instance."
            )
        return super().__new__(cls)

    @classmethod
    def get_instance(cls) -> "Config":
        """Return the singleton instance of the Config class."""
        if cls._instance is None:
            # Create the singleton instance
            cls._instance = cls()
        return cls._instance


# Usage
config = Config.get_instance()
