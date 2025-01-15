from dataclasses import dataclass
from decimal import Decimal

from domain.entities.wallets import Wallet as WalletEntity
from infra.database.models import WalletModel
from infra.repositories.wallets.base import BaseWalletRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select


@dataclass
class SQLAlchemyWalletRepository(BaseWalletRepository):
    async def update_balance(self, wallet_oid: str, amount: Decimal, session: AsyncSession):
        stmt = (
            update(WalletModel).where(WalletModel.oid == wallet_oid).values(
                balance=WalletModel.balance + amount
            )
        )
        await session.execute(stmt)

    async def get_by_oid(self, wallet_oid, session: AsyncSession) -> WalletEntity | None:
        result = await session.execute(select(WalletModel).where(WalletModel.oid == wallet_oid))
        wallet_model = result.scalars().one_or_none()
        if wallet_model:
            return WalletEntity(
                created_at=wallet_model.created_at,
                updated_at=wallet_model.updated_at,
                balance=wallet_model.balance,
                oid=wallet_model.oid,
            )
        
    
    async def add(self, wallet: WalletEntity, session: AsyncSession) -> WalletEntity:
        wallet_model = WalletModel(
            oid=wallet.oid,
        )
        
        session.add(wallet_model)
        await session.flush()

        return WalletEntity(
            oid=wallet_model.oid,
            balance=wallet_model.balance,
            created_at=wallet_model.created_at,
            updated_at=wallet_model.updated_at,
        )

