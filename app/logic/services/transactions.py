from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from application.api.filters import PaginationIn
from domain.entities.wallets import Transaction as TransactionEntity

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.transactions.base import BaseTransactionRepository
from logic.services.wallets import BaseWalletManagementService


@dataclass
class BaseTransactionService(ABC):
    @abstractmethod
    async def create_transaction(self, transaction: TransactionEntity) -> TransactionEntity: ...

    @abstractmethod
    async def get_transactions_list(self, wallet_oid: str, pagination: PaginationIn): ...


@dataclass
class TransactionService(BaseTransactionService):
    session_factory: sessionmaker
    transaction_repository: BaseTransactionRepository
    wallet_manager_service: BaseWalletManagementService

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        try:
            session: AsyncSession = self.session_factory()
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()

    
    async def create_transaction(self, transaction: TransactionEntity) -> TransactionEntity:
        async with self.get_session() as session:
           
            await self.wallet_manager_service._has_sufficient_funds(transaction=transaction, session=session)

            saved_transaction = await self.transaction_repository.add(transaction=transaction, session=session)

            await self.wallet_manager_service._update_wallet_amount(transaction=transaction, session=session)

        return saved_transaction
    
    async def get_transactions_list(self, wallet_oid: str, pagination: PaginationIn):
        async with self.get_session() as session:
            transactions = await self.transaction_repository.get_all(
                session=session, limit=pagination.limit, offset=pagination.offset, wallet_oid=wallet_oid
            )

        return transactions
    
