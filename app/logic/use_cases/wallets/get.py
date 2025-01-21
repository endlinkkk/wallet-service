from dataclasses import dataclass
from typing import Protocol

from domain.entities.wallets import Wallet as WalletEntity

# from logic.services.wallets import BaseWalletService
from logic.use_cases.base import BaseUseCase


class BaseWalletService(Protocol):
    async def get_wallet(self, wallet_oid: str) -> WalletEntity:
        pass

@dataclass
class GetWalletUseCase(BaseUseCase):
    wallet_service: BaseWalletService

    async def execute(self, wallet_oid: str) -> WalletEntity:
        wallet = await self.wallet_service.get_wallet(wallet_oid=wallet_oid)

        return wallet
