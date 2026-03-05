from abc import ABC, abstractmethod
from typing import Any


class Hasher(ABC):
    @staticmethod
    @abstractmethod
    def hash(data: Any) -> bytes: ...

    @staticmethod
    @abstractmethod
    def compare(hash_value: bytes, value: Any) -> bool: ...