from abc import ABC, abstractmethod
from typing import Any


class Hasher(ABC):
    @staticmethod
    @abstractmethod
    def hash(data: str) -> bytes | str: ...

    @staticmethod
    @abstractmethod
    def compare(hash_value: bytes | str, value: str) -> bool: ...