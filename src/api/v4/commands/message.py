from abc import abstractclassmethod
from command import Command
from arguments import Contact, Text


class MessageCreateCommand(Command):
    @abstractclassmethod
    def call(DefaultResponseCommand, exact_content: Text, recipient: Contact) -> None:
        raise NotImplementedError


