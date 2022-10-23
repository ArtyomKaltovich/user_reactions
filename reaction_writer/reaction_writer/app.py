from fastapi import FastAPI

from reaction_writer.io.writer.abc import ReactionWriterABC
from reaction_writer.io.writer.postgress.reaction_writer import (
    PostgresReactionWriter,
)
from reaction_writer.types import Username, Reaction, Timestamp
from settings import Settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    settings = Settings()
    reaction_writer = PostgresReactionWriter(
        settings.dbname,
        settings.dbuser,
        settings.dbpassword,
        settings.dbhost,
        settings.dbport,
        settings.dbpool_min_size,
        settings.dbpool_max_size,
        settings.dbpool_command_timeout,
        settings.debug,
    )
    app.state.reaction_writer = reaction_writer
    await reaction_writer.connect()


@app.get("/")
async def root():
    return {"message": "service has started"}


@app.post("/analytics/{timestamp}/{username}/{reaction}")
async def post_analytics(
        timestamp: Timestamp,
        username: Username,
        reaction: Reaction,
):
    reaction_writer: ReactionWriterABC = app.state.reaction_writer
    await reaction_writer.write(username, reaction, timestamp)
