from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseUseCase(ABC):
    @abstractmethod
    async def execute(self): ...
