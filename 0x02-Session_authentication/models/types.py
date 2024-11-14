#!/usr/bin/env python3
"""
Types module for defining generic types used throughout the project.

This module defines type aliases using `TypeVar` to represent generic types
that can be used across the project for better type hinting and flexibility.

These type aliases are primarily used for defining flexible
function signatures and ensuring type safety in areas where
the specific type is not known ahead of time.
"""
from typing import TypeVar

BaseType = TypeVar('BaseType')
UserType = TypeVar('UserType')
