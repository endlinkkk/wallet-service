from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class TransactionNotFoundException(LogicException):
    @property
    def message(self):
        return "Transaction not found"
