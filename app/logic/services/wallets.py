from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.wallets import (
    OperationType,
    Transaction as TransactionEntity,
    Wallet as WalletEntity,
)
from infra.database.manager import SessionManager
from infra.repositories.wallets.base import BaseWalletRepository
from logic.exceptions.wallets import (
    NotEnoughFundsException,
    WalletNotFoundException,
)


@dataclass
class BaseWalletManagementService(ABC):
    @abstractmethod
    async def _get_wallet_by_oid(self, wallet_oid: str) -> WalletEntity: ...

    @abstractmethod
    async def _has_sufficient_funds(self, transaction: TransactionEntity): ...

    @abstractmethod
    async def _update_wallet_amount(self, transaction: TransactionEntity): ...


@dataclass
class BaseWalletService(ABC):
    @abstractmethod
    async def get_wallet(self, wallet_oid: str) -> Decimal: ...

    @abstractmethod
    async def create_wallet(self, wallet: WalletEntity) -> WalletEntity: ...


@dataclass
class WalletManagementService(BaseWalletManagementService):
    wallet_repository: BaseWalletRepository

    async def _has_sufficient_funds(self, transaction: TransactionEntity, session: AsyncSession):
        wallet = await self.wallet_repository.get_wallet_with_lock(wallet_oid=transaction.wallet_oid, session=session)
        if wallet is None:
            raise WalletNotFoundException()
        if transaction.operation_type == OperationType.WITHDRAW and wallet.balance < transaction.amount:
            raise NotEnoughFundsException()

    async def _get_wallet_by_oid(self, wallet_oid: str, session: AsyncSession) -> WalletEntity:
        wallet = await self.wallet_repository.get_by_oid(wallet_oid=wallet_oid, session=session)

        if wallet is None:
            raise WalletNotFoundException()

        return wallet

    async def _update_wallet_amount(self, transaction: TransactionEntity, session: AsyncSession):
        amount = transaction.amount if transaction.operation_type == OperationType.DEPOSIT else -transaction.amount
        await self.wallet_repository.update_balance(
            wallet_oid=transaction.wallet_oid,
            session=session,
            amount=amount,
        )


@dataclass
class WalletService(BaseWalletService):
    session_manager: SessionManager
    wallet_repository: BaseWalletRepository

    async def get_wallet(self, wallet_oid: str) -> WalletEntity:
        async with self.session_manager as session:
            wallet = await self.wallet_repository.get_by_oid(wallet_oid=wallet_oid, session=session)
            if wallet is None:
                raise WalletNotFoundException()

        return wallet

    async def create_wallet(self, wallet: WalletEntity) -> WalletEntity:
        async with self.session_manager as session:
            wallet = await self.wallet_repository.add(wallet=wallet, session=session)

        return wallet
