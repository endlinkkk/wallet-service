from dataclasses import dataclass

from domain.entities.wallets import Wallet as WalletEntity

from logic.services.wallets import BaseWalletService
from logic.use_cases.base import BaseUseCase


@dataclass
class CreateWalletUseCase(BaseUseCase):
    wallet_service: BaseWalletService

    async def execute(self, wallet: WalletEntity) -> WalletEntity:
        created_wallet = await self.wallet_service.create_wallet(wallet=wallet)

        return created_wallet
