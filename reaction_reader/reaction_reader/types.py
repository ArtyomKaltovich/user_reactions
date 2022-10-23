import datetime
from typing import TypeVar, Dict

Timestamp = TypeVar("Timestamp", bound=int)
UserReactionInfo = TypeVar("UserReactionInfo", bound=str)
Cache = Dict[datetime.datetime, UserReactionInfo]


def create_user_reaction_info(
    n_unique_users: int = 0,
    n_clicks: int = 0,
    n_impressions: int = 0,
) -> str:
    return f"unique_users,{n_unique_users}\n" \
           f"clicks,{n_clicks}\n" \
           f"impressions,{n_impressions}\n"
