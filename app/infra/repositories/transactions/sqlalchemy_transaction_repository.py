from dataclasses import dataclass

from domain.entities.wallets import Transaction as TransactionEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from infra.database.models import TransactionModel
from infra.repositories.transactions.base import BaseTransactionRepository


@dataclass
class SQLAlchemyTransactionRepository(BaseTransactionRepository):
    async def add(self, transaction: TransactionEntity, session: AsyncSession) -> TransactionEntity:
        transaction_model = TransactionModel(
            oid=transaction.oid,
            amount=transaction.amount,
            operation_type=transaction.operation_type,
            wallet_oid=transaction.wallet_oid,
        )
        session.add(transaction_model)
        await session.flush()

        return TransactionEntity(
            oid=transaction_model.oid,
            created_at=transaction_model.created_at,
            amount=transaction_model.amount,
            operation_type=transaction_model.operation_type,
            wallet_oid=transaction_model.wallet_oid,
        )

    async def get_all(
        self, wallet_oid: str, session: AsyncSession, limit: int = 20, offset: int = 0
    ) -> list[TransactionEntity]:
        result = await session.execute(
            select(TransactionModel).where(TransactionModel.wallet_oid == wallet_oid).offset(offset).limit(limit)
        )

        transactions_models = result.scalars().all()

        return [
            TransactionEntity(
                oid=transaction_model.oid,
                created_at=transaction_model.created_at,
                amount=transaction_model.amount,
                operation_type=transaction_model.operation_type,
                wallet_oid=transaction_model.wallet_oid,
            )
            for transaction_model in transactions_models
        ]
