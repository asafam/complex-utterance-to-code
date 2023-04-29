import datetime
from typing import Type
from contact import Contact


class Message:
    
    @classmethod
    def get(cls, sender: Contact, date_time: str, location: str, category: str) -> Event:
        """
        Returns a message object
        
        Parameters:
        
        sender (Contact): the message's sender
        date_time (str): the event's date and time
        exact_content (str): the message's exact content
        
        Returns:
        
        Message 
        """
        pass
    
    @classmethod
    def list(cls, sender: Contact, date_time: str, location: str, category: str) -> list[Event]:
        """
        Returns a list of messages
        
        Parameters:
        
        sender (Contact): the message's sender
        date_time (str): the event's date and time
        exact_content (str): the message's exact content
        
        Returns:
        
        list[Message] 
        """
        pass
    
    def create(self, recepient: Contact, date_time: str, exact_content: str) -> Message:
        """
        Creates a message
        
        Parameters:
        
        recepient (Contact): the message's recepient
        date_time (str): the event's date and time
        exact_content (str): the message's exact content
        
        Returns:
        
        Message
        """
        pass
    
    def delete(self, recepient: Contact, date_time: str, exact_content: str) -> None:
        """
        Deletes a message
        
        Parameters:
        
        recepient (Contact): the message's recepient
        date_time (str): the event's date and time
        exact_content (str): the message's exact content
        
        Returns:
        
        list[Message] 
        """
        pass   
    
    def send(self, recepient: Contact, date_time: str, exact_content: str) -> None:
        """
        Sends a message
        
        Parameters:
        
        recepient (Contact): the message's recepient
        date_time (str): the event's date and time
        exact_content (str): the message's exact content
        
        Returns:
        
        None
        """
        pass
    
    def react(self, date_time: str, exact_content: str) -> None:
        """
        React to a message
        
        Parameters:
        
        date_time (str): the event's date and time
        exact_content (str): the message's exact content
        
        Returns:
        
        None 
        """
        pass