from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime


class Encoder(ABC):
    @abstractmethod
    def encode(self, payload: Dict[str, Any], expired_at: datetime) -> str: ...