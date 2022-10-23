import asyncio
import datetime
from collections import defaultdict

import pytz
from fastapi import FastAPI

from reaction_reader.cache import update_cache_task
from reaction_reader.io.reader.postgress.reaction_read import (
    PostgresReactionReader,
)
from reaction_reader.types import Timestamp, Cache, create_user_reaction_info
from settings import Settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    settings = Settings()
    reaction_reader = PostgresReactionReader(
        settings.dbname,
        settings.dbuser,
        settings.dbpassword,
        settings.dbhost,
        settings.dbport,
        settings.dbcommand_timeout,
        settings.debug,
    )
    app.state.reaction_reader = reaction_reader
    await reaction_reader.connect()
    app.state.cache = defaultdict(create_user_reaction_info)
    app.state.update_task = asyncio.create_task(
        update_cache_task(
            reaction_reader,
            app.state.cache,
            settings.update_reactions_period,
        )
    )


@app.on_event("shutdown")
async def shutdown():
    task: asyncio.Task = app.state.update_task
    task.cancel()
    await app.state.reaction_reader.close()


@app.get("/")
async def root():
    return {"message": "service has started"}


@app.get("/analytics")
async def get_analytics(
    timestamp: Timestamp,
):
    cache: Cache = app.state.cache
    t = datetime.datetime.fromtimestamp(
        timestamp / 1000,  # request timestamp in millis
        tz=pytz.timezone("utc"),
    )
    t = t.replace(minute=0, second=0, microsecond=0)
    return cache[t]
