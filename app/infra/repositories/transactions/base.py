from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.wallets import Transaction as TransactionEntity


@dataclass
class BaseTransactionRepository(ABC):
    @abstractmethod
    async def add(self, transaction: TransactionEntity) -> TransactionEntity: ...

    @abstractmethod
    async def get_all(self, wallet_oid: str, limit: int = 20, offset: int = 0) -> Iterable[TransactionEntity]: ...

