from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    async def is_valid(self) -> bool: ...