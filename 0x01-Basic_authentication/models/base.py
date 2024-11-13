#!/usr/bin/env python3
""" Base module """
import os
from datetime import datetime
from typing import List, Iterable, Dict, Any, Optional
import json
import uuid

from models.types import BaseType

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class Base:
    """ Base class for handling common operations """

    _storage = {}

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        """ Initialize a Base instance """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

        if isinstance(self.created_at, str):
            self.created_at = datetime.strptime(
                self.created_at, TIMESTAMP_FORMAT)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.strptime(
                self.updated_at, TIMESTAMP_FORMAT)

        # Ensure class-level storage exists
        self.__class__.init_storage()

    def __eq__(self, other: BaseType) -> bool:
        """ Check equality based on ID """
        return isinstance(other, Base) and self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert object to JSON representation """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue

            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value

        return result

    @classmethod
    def init_storage(cls) -> None:
        """ Initialize storage for the class if not already initialized """
        if not hasattr(cls, '_storage'):
            cls._storage = {}

    @classmethod
    def load_from_file(cls) -> None:
        """ Load objects from file into storage """
        file_path = f".db_{cls.__name__}.json"
        if not os.path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                cls._storage[obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls) -> None:
        """ Save all objects to file """
        file_path = f".db_{cls.__name__}.json"
        objs_json = {
            obj_id: obj.to_json(True) for
            obj_id, obj in cls._storage.items()
        }

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self) -> None:
        """ Save current object to storage """
        self.updated_at = datetime.utcnow()
        self.__class__._storage[self.id] = self
        self.__class__.save_to_file()

    def remove(self) -> None:
        """ Remove object from storage """
        if self.id in self.__class__._storage:
            del self.__class__._storage[self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Return count of all objects """
        return len(cls._storage)

    @classmethod
    def all(cls) -> Iterable[BaseType]:
        """ Return all objects """
        return list(cls._storage.values())

    @classmethod
    def get(cls, obj_id: str) -> Optional[BaseType]:
        """ Get object by ID """
        return cls._storage.get(obj_id, None)

    @classmethod
    def search(cls, attributes: Optional[Dict]) -> List[BaseType]:
        """ Search objects by attributes """
        if attributes is None:
            attributes = {}

        return [obj for obj in cls._storage.values()
                if all(getattr(obj, k) == v
                for k, v in attributes.items())]
