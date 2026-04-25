from abc import ABC, abstractmethod
from typing import Any, Dict


class Producer(ABC):
    @abstractmethod
    def send(self, title: str, payload: Dict[str, Any]):
        ...
