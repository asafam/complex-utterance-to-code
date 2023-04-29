import datetime
from contact import Contact


class Reminder:
    
    @classmethod
    def get(cls, title: str, person_reminded: str, date_time: str, location: str, recurring: bool) -> Reminder:
        """
        Returns a reminder object
        
        Parameters:
        
        title (str): the reminder's title
        person_reminded (Contact): the reminder's owner
        date_time (str): the event's date and time
        location (str): the reminder's associated location
        recurring (bool): a flag whether the reminder is recurring
        
        Returns:
        
        Reminder 
        """
        pass
    
    @classmethod
    def list(cls, title: str, person_reminded: str, date_time: str, location: str, recurring: bool) -> list[Reminder]:
        """
        Returns a list of reminders
        
        Parameters:
        
        title (str): the reminder's title
        person_reminded (Contact): the reminder's owner
        date_time (str): the event's date and time
        location (str): the reminder's associated location
        recurring (bool): a flag whether the reminder is recurring
        
        Returns:
        
        list[Reminder] 
        """
        pass
    
    def create(self, title: str, person_reminded: str, date_time: str, location: str, recurring: bool) -> Reminder:
        """
        Creates a reminder
        
        Parameters:
        
        title (str): the reminder's title
        person_reminded (Contact): the reminder's owner
        date_time (str): the event's date and time
        location (str): the reminder's associated location
        recurring (bool): a flag whether the reminder is recurring
        
        Returns:
        
        Reminder
        """
        pass
    
    def delete(self, recepient: Contact, date_time: str, exact_content: str) -> None:
        """
        Deletes a reminder
        
        Parameters:
        
        title (str): the reminder's title
        person_reminded (Contact): the reminder's owner
        date_time (str): the event's date and time
        location (str): the reminder's associated location
        recurring (bool): a flag whether the reminder is recurring
        
        Returns:
        
        list[Message] 
        """
        pass   
    