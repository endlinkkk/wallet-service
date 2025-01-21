from dataclasses import dataclass
from typing import Protocol

from domain.entities.wallets import Wallet as WalletEntity

# from logic.services.wallets import BaseWalletService
from logic.use_cases.base import BaseUseCase


class BaseWalletService(Protocol):
    async def create_wallet(self, wallet: WalletEntity) -> WalletEntity:
        pass

@dataclass
class CreateWalletUseCase(BaseUseCase):
    wallet_service: BaseWalletService

    async def execute(self, wallet: WalletEntity) -> WalletEntity:
        created_wallet = await self.wallet_service.create_wallet(wallet=wallet)

        return created_wallet
