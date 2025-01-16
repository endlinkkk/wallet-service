from datetime import datetime
from decimal import Decimal

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.wallets import (
    OperationType,
)
from domain.entities.wallets import (
    Transaction as TransactionEntity,
)
from domain.entities.wallets import (
    Wallet as WalletEntity,
)
from pydantic import BaseModel


class InTransactionSchema(BaseModel):
    operationType: OperationType  # noqa: N815
    amount: Decimal

    def to_entity(self, wallet_oid: str) -> TransactionEntity:
        return TransactionEntity(
            operation_type=self.operationType,
            amount=self.amount,
            wallet_oid=wallet_oid,
        )


class OutTransactionSchema(BaseModel):
    operationType: OperationType  # noqa: N815
    amount: Decimal
    created_at: datetime

    @classmethod
    def from_entity(cls, transaction: TransactionEntity) -> "OutTransactionSchema":
        return cls(
            operationType=transaction.operation_type,
            amount=transaction.amount,
            created_at=transaction.created_at,
        )


class InWalletSchema(BaseModel):
    def to_entity(self) -> WalletEntity:
        return WalletEntity()


class OutWalletSchema(BaseModel):
    uuid: str
    balance: Decimal
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, wallet: WalletEntity) -> "OutWalletSchema":
        return cls(
            uuid=wallet.oid,
            balance=wallet.balance,
            created_at=wallet.created_at,
            updated_at=wallet.updated_at,
        )


class GetTransactionsQueryResponseSchema(
    BaseQueryResponseSchema[list[OutTransactionSchema]],
): ...
