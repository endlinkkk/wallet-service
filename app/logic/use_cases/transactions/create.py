from dataclasses import dataclass
from typing import Protocol

from domain.entities.wallets import Transaction as TransactionEntity

# from logic.services.transactions import BaseTransactionService
from logic.use_cases.base import BaseUseCase


# from logic.validators.transactions import BaseTransactionValidatorService


class BaseTransactionService(Protocol):
    async def create_transaction(self, transaction: TransactionEntity) -> TransactionEntity:
        pass


class BaseTransactionValidatorService(Protocol):
    def validate(self, transaction: TransactionEntity):
        pass


@dataclass
class CreateTransactionUseCase(BaseUseCase):
    transaction_service: BaseTransactionService
    validator_service: BaseTransactionValidatorService

    async def execute(self, transaction: TransactionEntity) -> TransactionEntity:
        self.validator_service.validate(transaction=transaction)

        complited_transaction = await self.transaction_service.create_transaction(transaction=transaction)

        return complited_transaction
