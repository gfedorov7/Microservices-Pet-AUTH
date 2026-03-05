from abc import ABC, abstractmethod
from typing import Dict


class Decoder(ABC):
    @abstractmethod
    def decode(self, token: str) -> Dict[str, any]: ...