from document import Doc
from models.calendar import CalendarModel
from models.contacts import ContactsModel
from models.events import EventsModel
from models.locations import LocationsModel
from models.messages import MessagesModel
from models.navigation import DirectionsModel
from models.reminders import RemindersModel
from models.timer import TimerModel
from models.weather import WeatherModel
from commands.message import MessageCreateCommand
from commands.reminder import ReminderCreateCommand, ReminderDeleteCommand
from commands.response import DefaultResponseCommand, VoiceResponseCommand
from commands.timer import TimerPauseCommand, TimerRestartCommand, TimerStopCommand
from arguments import (
    CalendarEvent,
    Contact,
    DateTime,
    EventAvailability,
    EventCategory,
    Location,
    Reminder,
    Timer,
    Text,
)


"""
Example: "Tell me every stand up show tonight at 8 pm in the city"
"""
doc = Doc("Tell me every stand up show tonight at 8 pm in the city")

locations_model = LocationsModel(doc.text("the city"))
locations = iter(locations_model)
the_city = filter(
    locations_model.get_predicate(
        location=Location.resolve_from_document(doc=doc.text("the city"))
    ),
    locations,
)
the_city = sorted(the_city)


events_model = EventsModel(doc.text("every stand up show tonight at 8 pm in the city"))
events = iter(events_model)
stand_up_shows = filter(
    lambda x: events_model.get_predicate(
        category=EventCategory.resolve_from_document(doc=doc.text("stand up show"))
    )(x)
    and events_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("tonight"))
    )(x)
    and events_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("at 8 pm"))
    )(x)
    and events_model.get_predicate(
        location=Location.resolve_from_entities(entities=the_city)
    )(x),
    events,
)
stand_up_shows = sorted(stand_up_shows)

command = DefaultResponseCommand(
    doc.text("Tell me every stand up show tonight at 8 pm in the city")
)
command.call(content=Text.resolve_from_entities(entities=stand_up_shows))


"""
Example: "Create a reminder for the appointment while cancelling all other reminders for today"
"""
doc = Doc(
    "Create a reminder for the appointment while cancelling all other reminders for today"
)

calendar_model = CalendarModel(doc.text("the appointment"))
cal_events = iter(calendar_model)
the_appointment = filter(
    calendar_model.get_predicate(
        event=CalendarEvent.resolve_from_document(doc=doc.text("the appointment"))
    ),
    cal_events,
)
the_appointment = sorted(the_appointment)

command1 = ReminderCreateCommand(doc.text("Create a reminder for the appointment"))
command1.call(todo=Reminder.resolve_from_entities(entities=the_appointment))

reminders_model = RemindersModel(doc.text("all other reminders for today"))
reminders = iter(reminders_model)
other_reminders = filter(
    lambda x: reminders_model.get_predicate(
        RemindersModel.params.Reminder, "all other reminders"
    )(x)
    and reminders_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("for today"))
    ),
    reminders,
)
other_reminders = sorted(other_reminders)

command2 = ReminderDeleteCommand(doc.text("cancelling all other reminders for today"))
command2.call(reminders=Reminder.resolve_from_entities(entities=other_reminders))


"""
Example: "Text mom and dad about the Saturday brunch and the matinee"
"""
doc = Doc("Text mom and dad about the Saturday brunch and matinee")

contacts_model = ContactsModel(doc.text("mom"))
contacts = iter(contacts_model)
mom = filter(
    contacts_model.get_predicate(
        contact=Contact.resolve_from_document(doc=doc.text("mom"))
    ),
    contacts,
)
mom = sorted(mom)

contacts_model = ContactsModel(doc.text("dad"))
contacts = iter(contacts_model)
dad = filter(
    contacts_model.get_predicate(
        contact=Contact.resolve_from_document(doc=doc.text("dad"))
    ),
    contacts,
)
dad = sorted(dad)

calendar_model = CalendarModel(doc.text("the Saturday brunch"))
cal_events = iter(calendar_model)
saturday_brunch = filter(
    lambda x: calendar_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("Saturday"))
    )(x)
    and calendar_model.get_predicate(
        event=CalendarEvent.resolve_from_document(doc="brunch")
    )(x),
    cal_events,
)
saturday_brunch = sorted(saturday_brunch)

calendar_model = CalendarModel(doc.text("the matinee"))
cal_events = iter(calendar_model)
matinee = filter(
    calendar_model.get_predicate(
        event=CalendarEvent.resolve_from_document(doc="matinee")
    ),
    cal_events,
)
matinee = sorted(matinee)

for contact in [mom, dad]:
    for calendar_event in [matinee, saturday_brunch]:
        command = MessageCreateCommand(
            doc.text("Text mom and dad about the Saturday brunch and matinee")
        )
        command.call(
            recipient=Contact.resolve_from_entities(entities=contact),
            exact_content=Text.resolve_from_entities(entities=calendar_event),
        )
