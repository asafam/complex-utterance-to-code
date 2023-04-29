from abc import abstractmethod
from typing import Optional
from command import Command
from arguments import Text


class DefaultResponseCommand(Command):
    @abstractmethod
    def call(self, content: Text) -> None:
        pass


class VoiceResponseCommand(Command):
    @abstractmethod
    def call(self, content: Text) -> None:
        pass
