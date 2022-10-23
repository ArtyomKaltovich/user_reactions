from typing import Literal, TypeVar, get_args

Timestamp = TypeVar("Timestamp", bound=int)
Reaction = Literal["click", "impression"]
REACTIONS = get_args(Reaction)
Username = TypeVar("Username", bound=str)
