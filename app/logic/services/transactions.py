from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Iterable
from dataclasses import dataclass

from application.api.filters import PaginationIn
from domain.entities.wallets import Transaction as TransactionEntity
from infra.database.manager import SessionManager
from infra.repositories.transactions.base import BaseTransactionRepository
from logic.services.wallets import BaseWalletManagementService


@dataclass
class BaseTransactionService(ABC):
    @abstractmethod
    async def create_transaction(self, transaction: TransactionEntity) -> TransactionEntity: ...

    @abstractmethod
    async def get_transactions_list(
        self, wallet_oid: str,
        pagination: PaginationIn,
    ) -> Iterable[TransactionEntity]: ...


@dataclass
class TransactionService(BaseTransactionService):
    session_manager: SessionManager
    transaction_repository: BaseTransactionRepository
    wallet_manager_service: BaseWalletManagementService


    async def create_transaction(self, transaction: TransactionEntity) -> TransactionEntity:
        async with self.session_manager as session:
            await self.wallet_manager_service._has_sufficient_funds(transaction=transaction, session=session)

            saved_transaction = await self.transaction_repository.add(transaction=transaction, session=session)

            await self.wallet_manager_service._update_wallet_amount(transaction=transaction, session=session)

        return saved_transaction

    async def get_transactions_list(self, wallet_oid: str, pagination: PaginationIn) -> list[TransactionEntity]:
        async with self.session_manager as session:
            transactions = await self.transaction_repository.get_all(
                session=session,
                limit=pagination.limit,
                offset=pagination.offset,
                wallet_oid=wallet_oid,
            )

        return transactions
