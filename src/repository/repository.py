from abc import ABC, abstractmethod
from typing import Dict, Sequence, Any
from src.util.type.model import ModelType


class Repository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> ModelType | None: ...

    @abstractmethod
    async def get(self, limit: int, offset: int) -> Sequence[ModelType] | None: ...

    @abstractmethod
    async def create(self, model: Dict[str, Any]) -> ModelType: ...

    @abstractmethod
    async def update(self, id: int, model: Dict[str, Any]) -> ModelType: ...

    @abstractmethod
    async def delete(self, id: int) -> None: ...

    @abstractmethod
    async def count(self) -> int: ...
