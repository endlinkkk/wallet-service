from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from decimal import Decimal

from domain.entities.wallets import Wallet as WalletEntity


@dataclass
class BaseWalletRepository(ABC):
    @abstractmethod
    async def update_balance(self, wallet_oid: str, amount: Decimal): ...

    @abstractmethod
    async def get_by_oid(self, wallet_oid: str) -> WalletEntity: ...

    @abstractmethod
    async def add(self, wallet: WalletEntity) -> WalletEntity: ...
