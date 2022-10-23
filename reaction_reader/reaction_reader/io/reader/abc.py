import abc


class ReactionReaderABC:
    @abc.abstractmethod
    async def read(self):
        """ read all user reactions """
