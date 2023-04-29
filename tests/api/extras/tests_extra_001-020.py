from entities.generic import *
from entities.events import *
from entities.message import *
from entities.music import *
from entities.navigation import *
from entities.reminder import *
from entities.shopping import *
from entities.weather import *
from actions.calendar import Calendar
from actions.clock import *
from actions.events import *
from actions.messages import Messages
from actions.music import Music
from actions.navigation import Navigation
from actions.reminders import Reminders
from actions.responder import Responder
from actions.shopping import Shopping
from actions.weather import Weather
from providers.data_model import DataModel
from datetime import datetime, timedelta
import utils


def test_e0():
    """
    Send Tyler a text saying hi and send one to Susan too.
    """
    # test data
    data_model = DataModel(reset=True)
    data_contact1 = Contact(text="Tyler", value="Tyler")
    data_model.append(data_contact1)
    data_contact2 = Contact(text="Susan", value="Susan")
    data_model.append(data_contact2)
    data_content = Content(text="hi", value="hi")
    data_model.append(data_content)

    # start code block to test
    recipient = Contact.resolve_from_text("Tyler")
    content = Content.resolve_from_text("hi")
    Messages.send_message(recipient=recipient, content=content)

    recipient = Contact.resolve_from_text("Susan")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    data_messages_lists = data_model.get_response([MessageEntity])
    assert len(data_messages_lists) == 2
    data_message1 = data_messages_lists[0]
    assert data_message1.data.get("recipient") == data_contact1
    assert data_message1.data.get("content") == data_content
    data_message2 = data_messages_lists[1]
    assert data_message2.data.get("recipient") == data_contact2
    assert data_message2.data.get("content") == data_content
    

def test_e1():
    """
    Add entry in the calendar for a lunch meeting with Jack tomorrow at 3 PM, also text Jack that we will be meeting at 3 PM for lunch.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(
        text="tomorrow at 3 PM",
        value=(datetime.now() + timedelta(days=1)).replace(hour=15, minute=0),
    )
    data_model.append(data_date_time)
    data_event_name = EventName(
        text="lunch meeting with Jack", value="lunch meeting with Jack"
    )
    data_model.append(data_event_name)
    data_recipient = Contact(text="Jack", value="Jack Smith")
    data_model.append(data_recipient)
    data_content_message = Content(
        text="we will be meeting at 3 PM for lunch",
        value="we will be meeting at 3 PM for lunch",
    )
    data_model.append(data_content_message)
    
    # start code block to test
    # end code block to test

    # assertions
    data_events = data_model.get_data(EventEntity)
    assert len(data_events) == 1
    data_event = data_events[0]
    assert data_event.data.get("date_time") == data_date_time
    assert data_event.data.get("event_name") == data_event_name

    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert data_message.data.get("recipient") == data_recipient
    assert data_message.data.get("content") == data_content_message



