from pathlib import Path
from typing import Optional

import asyncpg

from reaction_writer.io.writer.abc import ReactionWriterABC
from reaction_writer.types import Timestamp, Username, Reaction

QUERIES_DIR = Path(__file__).parent / "sql"
WRITE_REACTION_QUERY = (QUERIES_DIR / "write_reaction.sql").read_text()
WRITE_REACTION_PLAN_NAME = "write_reaction_plan"


class PostgresReactionWriter(ReactionWriterABC):
    def __init__(
            self,
            dbname: str,
            dbuser: str,
            dbpassword: str,
            dbhost: str,
            dbport: int = 5432,
            dbpool_min_size: int = 1,
            dbpool_max_size: int = 10,
            dbpool_command_timeout: int = 60,
            raise_errors: bool = True,
    ):
        self._dbname = dbname
        self._dbuser = dbuser
        self._dbpassword = dbpassword
        self._dbhost = dbhost
        self._dbport = dbport
        self._dbpool_min_size = dbpool_min_size
        self._dbpool_max_size = dbpool_max_size
        self._dbpool_command_timeout = dbpool_command_timeout
        self._raise_errors = raise_errors

        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                min_size=self._dbpool_min_size,
                max_size=self._dbpool_max_size,
                command_timeout=self._dbpool_command_timeout,
                host=self._dbhost,
                port=self._dbport,
                user=self._dbuser,
                password=self._dbpassword,
                database=self._dbname,
            )
        async with self._pool.acquire() as con:
            return await con.prepare(
                WRITE_REACTION_QUERY,
                name=WRITE_REACTION_PLAN_NAME,
            )

    async def write(
            self,
            username: Username,
            reaction: Reaction,
            timestamp: Timestamp,
    ) -> None:
        try:
            await self._pool.execute(  # type: ignore [union-attr]  # Item "None" of "Optional[Any]" has no attribute "execute"
                f"execute {WRITE_REACTION_PLAN_NAME} "
                f"('{username}', '{reaction}', {timestamp})"
            )
        except AttributeError:
            raise TypeError("Please call connect first")

    async def close(self):
        if self._pool:
            await self._pool.close()
        self._pool = None
