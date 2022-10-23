import asyncio

import pytz

from reaction_reader.io.reader.abc import ReactionReaderABC
from reaction_reader.types import Cache, create_user_reaction_info


async def update_cache(
        reader: ReactionReaderABC,
        cache: Cache,
):
    state = await reader.read()
    cache.clear()
    for r in state:
        t = r["t"].replace(tzinfo=pytz.timezone("utc"))
        cache[t] = create_user_reaction_info(
            r["n_uniqie_users"],
            r["n_clicks"],
            r["n_impressions"],
        )


async def update_cache_task(
        reader: ReactionReaderABC,
        cache: Cache,
        repeat_every: float,
):
    while True:
        await asyncio.wait((
            update_cache(reader, cache),
            asyncio.sleep(repeat_every)
        ))
