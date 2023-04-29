from typing import Type


class Event:
    
    @classmethod
    def get(cls, name: str, date_time: str, location: str, category: str) -> Event:
        """
        Returns an event object
        
        Parameters:
        
        name (str): the event's name
        date_time (str): the event's date and time
        location (str): the event's location
        catgory (str): the event's category
        
        Returns:
        
        Event 
        """
        pass
    
    @classmethod
    def list(cls, name: str, date_time: str, location: str, category: str) -> list[Event]:
        """
        Returns a list of events
        
        Parameters:
        
        name (str): the event's name
        date_time (str): the event's date and time
        location (str): the event's location
        catgory (str): the event's category
        
        Returns:
        
        list[Event] 
        """
        pass