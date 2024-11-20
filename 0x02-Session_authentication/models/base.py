#!/usr/bin/env python3
"""
Base class for handling common operations like storage, serialization,
and file-based persistence.
"""
import os
import io
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, cast

from models.types import BaseType

# Constants
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DEFAULT_FILE_PREFIX = ".db_"


class Base:
    """
    Base class for managing common operations like ID generation,
    timestamp handling, storage, and persistence.
    """

    _storage: Dict[str, 'Base'] = {}
    _file_prefix: str = DEFAULT_FILE_PREFIX

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """Initialize a Base instance with optional attributes."""
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now(timezone.utc))
        self.updated_at = kwargs.get('updated_at', datetime.now(timezone.utc))

        if isinstance(self.created_at, str):
            self.created_at = datetime.strptime(
                self.created_at, TIMESTAMP_FORMAT)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.strptime(
                self.updated_at, TIMESTAMP_FORMAT)

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
    def search(cls, attributes: Optional[Dict[str, Any]]) -> List[BaseType]:
        """Search for objects by attributes."""
        if not attributes:
            return list(cls._storage.values())

        return [
            obj for obj in cls._storage.values()
            if all(getattr(obj, k, None) == v for k, v in attributes.items())
        ]
