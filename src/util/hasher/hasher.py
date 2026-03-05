from abc import ABC, abstractmethod

class Hasher(ABC):
    @staticmethod
    @abstractmethod
    def hash(data: any) -> bytes: ...

    @staticmethod
    @abstractmethod
    def compare(hash_value: bytes, value: any) -> bool: ...