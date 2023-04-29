from abc import abstractclassmethod
from command import Command
from arguments import Timer


class CreateTimerCommand(Command):

    @abstractclassmethod
    def call(CreateTimerCommand, timer_name: Timer) -> None:
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
    


class TimerPauseCommand(Command):

    @abstractclassmethod
    def call(TimerPauseCommand, timer: Timer) -> None:
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
    
    
    
class TimerRestartCommand(Command):

    @abstractclassmethod
    def call(TimerRestartCommand, timer: Timer) -> None:
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
    
    
    
class TimerStopCommand(Command):

    @abstractclassmethod
    def call(TimerStopCommand, timer: Timer) -> None:
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
