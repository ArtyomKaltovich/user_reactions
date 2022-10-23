from pathlib import Path
from typing import Optional

import asyncpg

from reaction_reader.io.reader.abc import ReactionReaderABC

QUERIES_DIR = Path(__file__).parent / "sql"
READ_REACTION_QUERY = (QUERIES_DIR / "read_reaction.sql").read_text()
READ_REACTION_PLAN_NAME = "read_reaction_plan"


class PostgresReactionReader(ReactionReaderABC):
    def __init__(
            self,
            dbname: str,
            dbuser: str,
            dbpassword: str,
            dbhost: str,
            dbport: int = 5432,
            dbcommand_timeout: float = 30.0,
            raise_errors: bool = True,
    ):
        self._dbname = dbname
        self._dbuser = dbuser
        self._dbpassword = dbpassword
        self._dbhost = dbhost
        self._dbport = dbport
        self._dbcommand_timeout = dbcommand_timeout
        self._raise_errors = raise_errors
        # PreparedStatement
        self._connection: Optional[asyncpg.connection.Connection] = None
        self._stmt = None

    async def connect(self):
        if not self._connection:
            connection = await asyncpg.connect(
                host=self._dbhost,
                port=self._dbport,
                user=self._dbuser,
                password=self._dbpassword,
                database=self._dbname,
                command_timeout=self._dbcommand_timeout,
            )
            self._stmt = await connection.prepare(
                READ_REACTION_QUERY,
                name=READ_REACTION_PLAN_NAME,
            )
            self._connection = connection

    async def read(self):
        try:
            return await self._stmt.fetch()  # type: ignore [union-attr]  # Item "None" of "Optional[Any]" has no attribute "execute"
        except AttributeError:
            raise TypeError("Please call connect first")

    async def close(self):
        if self._connection:
            await self._connection.close()
        self._connection = None
