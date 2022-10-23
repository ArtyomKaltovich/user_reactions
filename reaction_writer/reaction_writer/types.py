from typing import Literal, TypeVar

Timestamp = TypeVar("Timestamp", bound=int)
Reaction = Literal["click", "impression"]
Username = TypeVar("Username", bound=str)
