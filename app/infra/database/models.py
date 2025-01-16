from datetime import datetime
from decimal import Decimal

from domain.entities.wallets import OperationType
from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class WalletModel(Base):
    __tablename__ = "wallets"

    oid: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    transactions: Mapped[list["TransactionModel"]] = relationship(
        "TransactionModel",
        back_populates="wallet",
        cascade="all, delete-orphan",
    )


class TransactionModel(Base):
    __tablename__ = "transactions"

    oid: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    operation_type: Mapped[OperationType] = mapped_column(Enum(OperationType), nullable=False)
    wallet_oid: Mapped[str] = mapped_column(ForeignKey("wallets.oid"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    wallet: Mapped["WalletModel"] = relationship("WalletModel", back_populates="transactions")

    __table_args__ = (
        Index("ix_transactions_wallet_oid", "wallet_oid"),
    )
