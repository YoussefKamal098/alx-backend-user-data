#!/usr/bin/env python3
"""
Base module providing functionality for object storage, serialization,
timestamp management, and persistence through file-based storage.

This module contains two main classes:

1. BaseType: Represents the base class for all objects stored in memory.
2. Query: A helper class to filter and query stored objects.

The module supports storing objects in memory (in the `_storage` dictionary)
and serializing them to and from JSON files for persistence. It also supports
operations like searching for objects based on attributes, as well as creating
and managing unique IDs for objects.

Classes:
    - Query: A query builder class for filtering, retrieving, and manipulating
      objects in storage.
    - Base: The base class for all stored objects, providing ID generation,
      timestamp handling, storage management, and persistence functionality.

Constants:
    - TIMESTAMP_FORMAT: The format used for datetime string serialization.
    - DEFAULT_FILE_PREFIX: Default prefix for the file name used for
      persistent storage.
"""
import os
import io
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, cast, Generator

from models.types import BaseType

# Constants
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_FILE_PREFIX = ".db_"


class Query:
    """
    A helper class to filter and query stored objects lazily.

    This class allows chaining methods like `first()`, `last()`, and `all()`
    to retrieve specific objects from storage based on the provided search
    criteria. Results are filtered lazily to improve performance.

    Attributes:
        model (type): The model class of the objects being queried.
        attributes (dict): The attributes to filter objects by.
        _results (list or None): Cached list of filtered results to avoid
                                 redundant filtering.
    """

    def __init__(
            self, model: type(BaseType), attributes: Optional[Dict[str, Any]]
    ):
        """
        Initialize the Query object with the model class and optional filter
        attributes.

        Args:
            model (type): The model class for which to query objects.
            attributes (Optional[Dict[str, Any]]): The attributes to filter
                                                   the objects by.
        """
        self.model = model
        self.attributes = attributes
        self._results = None  # To store results once they are computed

    def _filter_results(self) -> Generator[BaseType, None, None]:
        """
        Helper function to filter objects lazily based on
        the provided attributes.
        """
        if not self.attributes:
            # If no attributes, return all objects lazily
            yield from self.model.get_all_objects()
        else:
            # Otherwise, filter objects lazily based on attributes
            for obj in self.model.get_all_objects():
                if all(getattr(obj, k, None) == v
                       for k, v in self.attributes.items()):
                    yield obj

    def _get_results(self) -> List[BaseType]:
        """Filter the results and cache them for reuse."""
        if self._results is None:
            # Cache results after filtering
            self._results = list(self._filter_results())
        return self._results

    def first(self) -> BaseType:
        """Return the first object that matches the search criteria."""
        results = self._get_results()
        return results[0] if results else None

    def last(self) -> BaseType:
        """Return the last object that matches the search criteria."""
        results = self._get_results()
        return results[-1] if results else None

    def all(self) -> List[BaseType]:
        """Return all objects that match the search criteria."""
        return self._get_results()


class Base:
    """
    Base class for managing common operations like ID generation, timestamp
    handling, storage, and persistence.

    This class serves as the parent for all objects that need to be stored
    and retrieved from persistent storage (like a JSON file). It provides
    functionality for generating unique IDs, handling object timestamps,
    storing objects in memory, and saving them to or loading them from a file.

    Attributes:
        _storage (dict): A dictionary holding all objects of the class
            in memory.
        _file_prefix (str): The prefix used for the file name where objects are
                             stored.
        id (str): The unique identifier of the object.
        created_at (datetime): The timestamp of when the object was created.
        updated_at (datetime): The timestamp of the last update to the object.
    """

    _storage: Dict[str, 'Base'] = {}
    _file_prefix: str = DEFAULT_FILE_PREFIX

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """
        Initialize a Base instance with optional attributes.

        Args:
            id (str, optional): The unique identifier for the object. If not
                                 provided, a new UUID will be generated.
            created_at (datetime or str, optional): The timestamp of when the
                                                     object was created.
            updated_at (datetime or str, optional): The timestamp of the last
                                                     update to the object.
        """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now(timezone.utc))
        self.updated_at = kwargs.get('updated_at', datetime.now(timezone.utc))

        if isinstance(self.created_at, str):
            self.created_at = \
                datetime.strptime(self.created_at, TIMESTAMP_FORMAT)
        if isinstance(self.updated_at, str):
            self.updated_at = \
                datetime.strptime(self.updated_at, TIMESTAMP_FORMAT)

        # Ensure class-level storage exists
        self.__class__.init_storage()

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        """Helper method to parse datetime from string or return as-is."""
        if isinstance(value, str):
            return datetime.strptime(value, TIMESTAMP_FORMAT)
        return value

    def __eq__(self, other: BaseType) -> bool:
        """Check equality based on ID."""
        return isinstance(other, Base) and self.id == other.id

    def to_json(self, for_serialization: bool = False) -> Dict[str, Any]:
        """Convert object to JSON representation."""
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith("_"):
                continue

            result[key] = value.strftime(TIMESTAMP_FORMAT) if \
                isinstance(value, datetime) else value
        return result

    @classmethod
    def _get_file_path(cls) -> str:
        """Return the file path for storing objects."""
        return f"{cls._file_prefix}{cls.__name__}.json"

    @classmethod
    def init_storage(cls) -> None:
        """Initialize storage for the class if not already initialized."""
        if not hasattr(cls, "_storage"):
            cls._storage = {}

    @classmethod
    def load_from_file(cls) -> None:
        """Load objects from a file into storage."""
        file_path = cls._get_file_path()
        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as f:
            objects = json.load(f)
            cls._storage = {
                obj_id: cls(**obj_data)
                for obj_id, obj_data in objects.items()
            }

    @classmethod
    def save_to_file(cls) -> None:
        """Save all objects to a file."""
        file_path = cls._get_file_path()
        with open(file_path, "w") as f:
            json.dump({
                obj_id: obj.to_json(for_serialization=True)
                for obj_id, obj in cls._storage.items()
            }, cast(io.TextIOWrapper, f))

    def save(self) -> None:
        """Save the current object to storage."""
        self.updated_at = datetime.now(timezone.utc)
        self.__class__._storage[self.id] = self
        self.__class__.save_to_file()

    def remove(self) -> None:
        """Remove the object from storage."""
        if self.id in self.__class__._storage:
            del self.__class__._storage[self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Return the count of all objects."""
        return len(cls._storage)

    @classmethod
    def all(cls) -> List[BaseType]:
        """Return all objects."""
        return list(cls._storage.values())

    @classmethod
    def get(cls, obj_id: str) -> Optional[BaseType]:
        """Get an object by ID."""
        return cls._storage.get(obj_id)

    @classmethod
    def get_all_objects(cls) -> Generator['BaseType', None, None]:
        """Generator to yield all objects stored in the class."""
        for obj in cls._storage.values():
            yield obj

    @classmethod
    def search(cls, attributes: Optional[Dict[str, Any]] = None) -> 'Query':
        """Returns a Query object to chain additional
        methods like first(), last(), and all()"""
        return Query(cls, attributes)
