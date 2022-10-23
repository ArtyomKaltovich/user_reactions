import abc

from reaction_writer.types import Timestamp, Username, Reaction


class ReactionWriterABC:
    @abc.abstractmethod
    async def write(
            self,
            username: Username,
            reaction: Reaction,
            timestamp: Timestamp,
    ) -> None:
        """ write user's reaction to external storage """
