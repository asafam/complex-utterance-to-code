from sqlite3 import Date
from api.v4.arguments import AppName
from api.v4.models.navigation import EstimateDepartureModel
from document import Doc
from models.app import AppsModel
from models.calendar import CalendarModel
from models.contacts import ContactsModel
from models.events import EventsModel
from models.locations import LocationsModel
from models.messages import MessagesModel
from models.navigation import DirectionsModel, TrafficInfoModel
from models.reminders import RemindersModel
from models.timer import TimerModel
from models.weather import WeatherModel
from commands.app import AppOpenCommand
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
    TrafficCondition,
    WeatherCondition,
    WeatherTemperature,
)


"""
Example: "Remind me to bring a coat, if it rains"
"""

doc = Doc("Remind me to bring a coat, if it rains")

weather_model = WeatherModel(doc.text("rains"))
weather = iter(weather_model)
rainy_weather = filter(
    weather_model.get_predicate(
        weather_condition=WeatherCondition.resolve_from_document(doc=doc.text("rains"))
    ),
    weather,
)
rainy_weather = sorted(rainy_weather)

if len(list(rainy_weather)) > 0:
    contacts_model = ContactsModel(doc.text("me"))
    contacts = iter(contacts_model)
    me = filter(
        contacts_model.get_predicate(
            contact=Contact.resolve_from_document(doc=doc.text("me"))
        ),
        contacts,
    )
    me = sorted(me)

    command = ReminderCreateCommand(doc.text("Remind me to bring a coat"))
    command.call(
        person_reminded=Contact.resolve_from_entities(entities=me),
        todo=Reminder.resolve_from_document(doc=doc.text("to bring a coat")),
    )


# Example: "Provided that it rains tomorrow set a reminder to leave 15 minutes earlier"

doc = Doc("Provided that it rains tomorrow set a reminder to leave 15 minutes earlier")

weather_model = WeatherModel(doc.text("rains tomorrow"))
weather = iter(weather_model)
rainy_weather = filter(
    lambda x: weather_model.get_predicate(
        weather_condition=WeatherCondition.resolve_from_document(doc=doc.text("rains"))
    )(x)
    and weather_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("tomorrow"))
    )(x),
    weather,
)
rainy_weather = sorted(rainy_weather)

if len(list(rainy_weather)) > 0:
    command = ReminderCreateCommand(
        doc.text("set a reminder to leave 15 minutes earlier")
    )
    command.call(todo=doc.text("to leave 15 minutes earlier"))


# Exampe: "If it rains then remind me tonight to bring a coat at 11 pm, if it is less than 40 degrees"

weather_model = WeatherModel(doc.text("rains"))
weather = iter(weather_model)
rainy_weather = filter(
    weather_model.get_predicate(
        weather_condition=WeatherCondition.resolve_from_document(doc=doc.text("rains"))
    ),
    weather,
)
rainy_weather = sorted(rainy_weather)

if len(rainy_weather) > 0:
    weather_model = WeatherModel(doc.text("less than 40 degrees"))
    weather = iter(weather_model)
    temperature_40 = filter(
        weather_model.get_predicate(
            temperature=WeatherTemperature.resolve_from_document(
                doc=doc.text("less than 40 degrees")
            )
        ),
        weather,
    )
    temperature_40 = sorted(temperature_40)

    if len(list(temperature_40)) > 0:
        contacts_model = ContactsModel(doc.text("me"))
        contacts = iter(contacts_model)
        me = filter(
            contacts_model.get_predicate(
                contact=Contact.resolve_from_document(doc=doc.text("me"))
            ),
            contacts,
        )
        me = sorted(me)

        command = ReminderCreateCommand(doc.text("remind me tonight to bring a coat"))
        command.call(
            person_reminded=Contact.resolve_from_entities(entities=me),
            date_time=DateTime.resolve_from_document(
                doc=[doc.text("tonight"), doc.text("at 11 pm")]
            ),
            todo=Text.resolve_from_document(doc=doc.text("to bring a coat")),
        )


"""
Example: "If there is traffic in the city tell Mary that I will be late, otherwise tell her I will be on time"
"""

doc = Doc(
    "If there is traffic in the city tell Mary that I will be late, otherwise tell her I will be on time"
)

locations_model = LocationsModel(doc.text("the city"))
locations = iter(locations_model)
the_city = filter(
    locations_model.get_predicate(
        location=Location.resolve_from_document(doc=doc.text("the city"))
    ),
    locations,
)
the_city = sorted(the_city)

traffic_model = TrafficInfoModel(doc.text("traffic in the city"))
traffic = iter(traffic_model)
traffic_in_city = filter(
    lambda x: traffic_model.get_predicate(
        traffic_condition=TrafficCondition.resolve_from_document(
            doc=doc.text("traffic")
        )
    )(x)
    and traffic_model.get_predicate(
        destination=Location.resolve_from_entities(entities=the_city)
    )(x),
    traffic,
)
traffic_in_city = sorted(traffic_in_city)

if len(list(traffic_in_city)) > 0:
    contacts_model = ContactsModel(doc.text("Mary"))
    contacts = iter(contacts_model)
    mary = filter(
        contacts_model.get_predicate(
            contact=Contact.resolve_from_document(doc=doc.text("Mary"))
        ),
        contacts,
    )
    mary = sorted(mary)

    command = MessageCreateCommand(doc.text("tell Mary that I will be late"))
    command.call(
        recipient=Contact.resolve_from_entities(entities=mary),
        exact_content=Text.resolve_from_document(doc=doc.text("I will be late")),
    )
else:
    contacts_model = ContactsModel(doc.text("her"))
    contacts = iter(contacts_model)
    her = filter(
        contacts_model.get_predicate(
            contact=Contact.resolve_from_document(doc=doc.text("her"))
        ),
        contacts,
    )
    her = sorted(her)

    command = MessageCreateCommand(doc.text("tell her I will be on time"))
    command.call(
        recipient=Contact.resolve_from_entities(entities=her),
        exact_content=Text.resolve_from_document(doc=doc.text("I will be on time")),
    )


"""
Example: "Provided that I have a reminder or that I got a message from Jane, start me up the yoga app and tell me when I need to leave for class unless it's raining"
"""
doc = Doc(
    "Provided that I have a reminder or that I got a message from Jane, start me up the yoga app and tell me when I need to leave for class unless it's raining"
)

contacts_model = ContactsModel(doc.text("I"))
contacts = iter(contacts_model)
i = filter(
    contacts_model.get_predicate(
        contact=Contact.resolve_from_document(doc=doc.text("I"))
    ),
    contacts,
)
i = sorted(i)

reminders_model = RemindersModel(doc.text("I have a reminder"))
reminders = iter(reminders_model)
reminder = filter(
    reminders_model.get_predicate(
        person_reminded=Contact.resolve_from_entities(entities=i)
    ),
    reminders,
)
reminder = sorted(reminder)

contacts_model = ContactsModel(doc.text("Jane"))
contacts = iter(contacts_model)
jane = filter(
    contacts_model.get_predicate(
        contact=Contact.resolve_from_document(doc=doc.text("Jane"))
    ),
    contacts,
)
jane = sorted(jane)

messages_model = MessagesModel(doc.text("a message from Jane"))
messages = iter(messages_model)
jane_messages = filter(
    messages_model.get_predicate(sender=Contact.resolve_from_entities(entities=jane)),
    messages,
)
jane_messages = sorted(jane_messages)

if len(list(reminder)) > 0 or len(list(jane_messages)) > 0:
    apps_model = AppsModel(doc.text("the yoga app"))
    apps = iter(apps_model)
    yoga_app = filter(
        apps_model.get_predicate(
            app=AppName.resolve_from_document(doc=doc.text("the yoga app"))
        ),
        apps,
    )
    yoga_app = sorted(yoga_app)

    command1 = AppOpenCommand(doc.text("start me up the yoga app"))
    command1.call(app=AppName.resolve_from_entities(entities=yoga_app))

    weather_model = WeatherModel(doc.text("raining"))
    weather = iter(weather_model)
    raining = filter(
        weather_model.get_predicate(
            weather_condition=WeatherCondition.resolve_from_document(
                doc=doc.text("raining")
            )
        ),
        weather,
    )
    raining = sorted(raining)

    if not (len(list(raining)) > 0):
        locations_model = LocationsModel(doc.text("class"))
        locations = iter(locations_model)
        class_loc = filter(
            locations_model.get_predicate(
                location=Location.resolve_from_document(doc=doc.text("class"))
            ),
            locations,
        )
        class_loc = sorted(class_loc)

        departure_model = EstimateDepartureModel(
            doc.text("when I need to leave for class")
        )
        departures = iter(departure_model)
        class_departure = filter(
            departure_model.get_predicate(
                destination=Location.resolve_from_entities(entities=class_loc)
            ),
            departures,
        )
        class_departure = sorted(class_departure)

        command2 = DefaultResponseCommand(
            doc.text("tell me when I need to leave for class")
        )
        command2.call(content=Text.resolve_from_entities(entities=class_departure))
