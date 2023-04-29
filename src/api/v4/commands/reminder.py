from abc import abstractclassmethod
from command import Command
from arguments import Contact, DateTime, Reminder, Text


class ReminderCreateCommand(Command):

    @abstractclassmethod
    def call(ReminderDeleteCommand, date_time: DateTime, person_reminded: Contact, todo: Text) -> None:
        """
        An abstract method that binds a command parameter with a query and optionally with an entity

        params:
        param (Param): The command param indicating a semantic role
        query (Query): A user query associated with the semantic role param
        value_mapping (Mapping[Span, Entity]): Optional variable that allows the mapping of spans within a query to Entity values

        returns:
        None
        """
        raise NotImplementedError
    

class ReminderDeleteCommand(Command):

    @abstractclassmethod
    def call(ReminderDeleteCommand, reminders: Reminder) -> None:
        """
        An abstract method that binds a command parameter with a query and optionally with an entity

        params:
        param (Param): The command param indicating a semantic role
        query (Query): A user query associated with the semantic role param
        value_mapping (Mapping[Span, Entity]): Optional variable that allows the mapping of spans within a query to Entity values

        returns:
        None
        """
        raise NotImplementedError
    
