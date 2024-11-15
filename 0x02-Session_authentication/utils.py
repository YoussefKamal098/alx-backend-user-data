#!/usr/bin/env python3
"""
utils Module

This module provides utility functions and decorators that are commonly
used across different parts of the project. This includes the `@override`
decorator to enforce that methods must be overridden in subclasses.

The `override` decorator ensures that subclasses implement critical methods
that are required for the functionality of the application, raising a
`NotImplementedError` if the subclass fails to provide an implementation.

Functions:
    override:
        Decorator to enforce that a method must be overridden in a subclass.
"""

import functools


def override(method):
    """
    Decorator to enforce that a method must be overridden in a subclass.

    This decorator ensures that any subclass of a base class using
    the `@override` decorator must override the decorated method.
    If the subclass does not provide
    its implementation for the method, an error is raised.

    Args:
        method (function): The method to be decorated.

    Returns:
        function: The wrapper function that performs the override enforcement.

    Raises:
        NotImplementedError: If the method is not overridden in the subclass.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Check if the method exists in the subclass
        if method.__name__ in self.__class__.__dict__:
            # Ensure that the method is not the base class method
            if self.__class__.__dict__[method.__name__] is method:
                raise NotImplementedError(
                    f"The method `{method.__name__}` "
                    f"must be overridden in the subclass "
                    f"`{self.__class__.__name__}`."
                )
        else:
            # If the method is not implemented in the subclass, raise an error
            raise NotImplementedError(
                f"The method `{method.__name__}` "
                f"must be overridden in the subclass "
                f"`{self.__class__.__name__}`."
            )
        return method(self, *args, **kwargs)

    return wrapper
