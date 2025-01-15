from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class WalletNotFoundException(LogicException):
    @property
    def message(self):
        return "Wallet not found"
    

@dataclass
class NotEnoughFundsException(LogicException):
    @property
    def message(self):
        return "Not enough funds in wallet"