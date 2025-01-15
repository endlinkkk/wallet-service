from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from uuid import uuid4

from datetime import datetime

@dataclass
class BaseEntity:
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    


class OperationType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


@dataclass
class Wallet(BaseEntity):
    balance: Decimal = field(kw_only=True, default=0)
    updated_at: datetime | None = field(default=None)

@dataclass
class Transaction(BaseEntity):
    wallet_oid: str = field(kw_only=True)
    amount: Decimal = field(kw_only=True)
    operation_type: OperationType