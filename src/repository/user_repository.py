from abc import ABC, abstractmethod
from typing import Any

from src.repository.repository import Repository
from src.util.type.model import ModelType


class UserRepository(Repository, ABC):
    @abstractmethod
    async def get_by_login(self, login: str) -> ModelType | Any: ...
