from abc import ABC, abstractmethod
from typing import Any

from src.model.user import User
from src.repository.repository import Repository


class UserRepository(Repository):
    @abstractmethod
    async def get_by_login(self, login: str) -> User | Any: ...
