from collections.abc import Iterable
from dataclasses import dataclass

from application.api.filters import PaginationIn
from domain.entities.wallets import Transaction as TransactionEntity

from logic.services.transactions import BaseTransactionService
from logic.use_cases.base import BaseUseCase


@dataclass
class GetTransactionsUseCase(BaseUseCase):
    transaction_service: BaseTransactionService

    async def execute(self, wallet_oid: str, pagination: PaginationIn) -> Iterable[TransactionEntity]:
        transactions = await self.transaction_service.get_transactions_list(
            pagination=pagination, wallet_oid=wallet_oid
        )

        return transactions
