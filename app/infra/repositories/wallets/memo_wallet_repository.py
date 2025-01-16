from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from domain.entities.wallets import Wallet as WalletEntity

from infra.repositories.wallets.base import BaseWalletRepository


@dataclass
class MemoryWalletRepository(BaseWalletRepository):
    wallets: list[WalletEntity] = field(default_factory=list)

    async def update_balance(self, wallet_oid: str, amount: Decimal, *args, **kwargs):
        for wallet in self.wallets:
            if wallet.oid == wallet_oid:
                wallet.balance += amount
                break

    async def get_by_oid(self, wallet_oid, *args, **kwargs) -> WalletEntity | None:
        for wallet in self.wallets:
            if wallet.oid == wallet_oid:
                return wallet

    async def add(self, wallet: WalletEntity, *args, **kwargs) -> WalletEntity:
        wallet.created_at = datetime.now()
        wallet.updated_at = datetime.now()
        self.wallets.append(wallet)
        return wallet
