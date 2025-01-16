from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):  # noqa: N818
    @property
    def message(self):
        return "Application exception"


@dataclass
class InvalidOperationTypeException(ApplicationException):
    operation_type: str

    @property
    def message(self):
        return f"Invalid operation type: {self.operation_type}"


@dataclass
class TransactionAmountNegativeМalueException(ApplicationException):
    @property
    def message(self):
        return "Invalid transaction amount"
