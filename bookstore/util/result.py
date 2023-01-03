from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    code: int
    message: str
    data: Any

    @staticmethod
    def success(message: str, data: Any = None):
        return Result(code=200, message=message, data=data)

    @staticmethod
    def fail(message: str, data: Any = None):
        return Result(code=400, message=message, data=data)