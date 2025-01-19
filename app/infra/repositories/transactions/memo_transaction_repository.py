from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from domain.entities.wallets import Transaction as TransactionEntity
from infra.repositories.transactions.base import BaseTransactionRepository


@dataclass
class MemoryTransactionRepository(BaseTransactionRepository):
    transactions: list[TransactionEntity] = field(default_factory=list)

    async def add(self, transaction: TransactionEntity, *args, **kwargs) -> TransactionEntity:
        transaction.created_at = datetime.now()
        self.transactions.append(transaction)
        return transaction

    async def get_all(
        self,
        wallet_oid: str,
        limit: int = 20,
        offset: int = 0,
        *args,
        **kwargs,
    ) -> list[TransactionEntity]:
        result = [t for t in self.transactions if t.wallet_oid == wallet_oid]
        return result[offset : offset + limit]
