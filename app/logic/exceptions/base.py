from dataclasses import dataclass

from domain.exceptions import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException):
    @property
    def message(self):
        return "There was an error processing the request"

