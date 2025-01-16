from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.wallets import (
    OperationType,
)
from domain.entities.wallets import (
    Transaction as TransactionEntity,
)
from domain.exceptions import (
    InvalidOperationTypeException,
    TransactionAmountNegativeМalueException,
)


@dataclass
class BaseTransactionValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        transaction: TransactionEntity,
    ): ...


@dataclass
class TransactionAmountValidatorService(BaseTransactionValidatorService):
    def validate(self, transaction: TransactionEntity):
        if transaction.amount < 0:
            raise TransactionAmountNegativeМalueException()


@dataclass
class TransactionOperationTypeValidatorService(BaseTransactionValidatorService):
    def validate(self, transaction: TransactionEntity):
        if transaction.operation_type not in [OperationType.DEPOSIT, OperationType.WITHDRAW]:
            raise InvalidOperationTypeException(operation_type=transaction.operation_type)


@dataclass
class ComposedTaskValidatorService:
    validators: list[BaseTransactionValidatorService]

    def validate(self, transaction: TransactionEntity):
        for v in self.validators:
            v.validate(transaction=transaction)
