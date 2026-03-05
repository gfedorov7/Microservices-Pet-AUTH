from abc import ABC, abstractmethod
from typing import Dict


class Encoder(ABC):
    @abstractmethod
    def encode(self, payload: Dict[str, Any]) -> str: ...