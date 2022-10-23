from typing import Literal, TypeVar

Timestamp = TypeVar("Timestamp", bound=str)
Reaction = Literal["click", "impression"]
Username = TypeVar("Username", bound=str)
