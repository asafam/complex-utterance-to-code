from entities.generic import *
from entities.message import *
from entities.navigation import *
from entities.reminder import *
from entities.weather import *
from actions.messages import Messages
from actions.navigation import Navigation
from actions.reminders import Reminders
from actions.responder import Responder
from actions.weather import Weather
from providers.data_model import DataModel
from datetime import datetime


def test_get_started_complex1():
    """
    What will the weather be in two hours, and remind me then to go running.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="in two hours", value=datetime(2022, 10, 8, 16, 15))
    data_model.append(data_date_time)
    data_model.append(WeatherForecastEntity(date_time=data_date_time))
    data_person_reminded = Contact(text="me", value="Louis Armstrong")
    data_model.append(data_person_reminded)
    data_content = Content(text="go running", value="go running")
    data_model.append(data_content)

    # code block to test
    date_time = DateTime.resolve_from_text("in two hours")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    content = Content.resolve_from_text("go running")
    person_reminded = Contact.resolve_from_text("me")
    Reminders.create_reminder(
        content=content, person_reminded=person_reminded, date_time=date_time
    )

    # assertions
    data_weather_forecasts_list = data_model.get_response([WeatherForecastEntity])
    assert len(data_weather_forecasts_list) > 0
    data_weather_forecasts = data_weather_forecasts_list[-1]
    assert len(list(data_weather_forecasts)) == 1
    assert list(data_weather_forecasts)[0].date_time == data_date_time

    data_reminder_list = data_model.get_data(ReminderEntity)
    assert len(data_reminder_list) == 1
    data_reminder = data_reminder_list[0]
    assert data_reminder.content == data_content
    assert data_reminder.person_reminded == data_person_reminded
    assert data_reminder.date_time == data_date_time


def test_get_started_complex2():
    """
    Get directions from Disneyland to my house and text them to Robert.
    """
    # test data
    data_model = DataModel(reset=True)
    data_origin = Location(text="Disneyland", value="Disneyland")
    data_model.append(data_origin)
    data_destination = Location(text="my house", value="my house")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(
        origin=data_origin,
        destination=data_destination,
    )
    data_model.append(data_navigation_direction)
    data_model.append(
        NavigationDirectionEntity(
            origin=data_destination,
            destination=data_origin,
        )
    )
    data_recipient = Contact(text="Robert", value="Robert")
    data_model.append(data_recipient)
    data_content = Content(value=[data_navigation_direction])
    data_model.append(data_content)

    # code block to be tested
    origin = Location.resolve_from_text("Disneyland")
    destination = Location.resolve_from_text("my house")
    navigation_directions = Navigation.find_directions(
        origin=origin, destination=destination
    )

    recipient = Contact.resolve_from_text("Robert")
    content = Content.resolve_from_entity(navigation_directions)
    message = Messages.send_message(recipient=recipient, content=content)

    # assertions
    data_messages_list = data_model.get_data(MessageEntity)
    assert len(data_messages_list) == 1
    data_message = data_messages_list[0]
    assert data_message.recipient == data_recipient
    assert data_message.content == data_content


def test_get_started_complex3a():
    """
    Remind me to bring an umbrella if it rains tomorrow.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rains", value="rain")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(text="tomorrow", value=datetime(2022, 10, 12, 0, 0))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time
        )
    )
    data_person_reminded = Contact(text="me", value="Me")
    data_model.append(data_person_reminded)
    data_content = Content(text="bring an umbrella", value="bring an umbrella")
    data_model.append(data_content)

    # code block to be tested
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_attribute = WeatherAttribute.resolve_from_text("rains")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    test = len(list(weather_forecasts)) > 0
    if test:
        person_reminded = Contact.resolve_from_text("me")
        content = Content.resolve_from_text("bring an umbrella")
        reminder = Reminders.create_reminder(
            person_reminded=person_reminded, content=content
        )

    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(list(data_reminders)) == 1
    data_reminder = data_reminders[0]
    assert data_reminder.person_reminded == data_person_reminded
    assert data_reminder.content == data_content


def test_get_started_complex3b():
    """
    Remind me to bring an umbrella if it rains tomorrow.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="rains", value="rain")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="sunny", value="sun")
    data_model.append(data_weather_attribute2)
    data_date_time = DateTime(text="tomorrow", value=datetime(2022, 10, 12, 0, 0))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute2, date_time=data_date_time
        )
    )
    data_person_reminded = Contact(text="me", value="Me")
    data_model.append(data_person_reminded)
    data_content = Content(text="bring an umbrella", value="bring an umbrella")
    data_model.append(data_content)

    # code block to be tested
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_attribute = WeatherAttribute.resolve_from_text("rains")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        person_reminded = Contact.resolve_from_text("me")
        content = Content.resolve_from_text("bring an umbrella")
        reminder = Reminders.create_reminder(
            person_reminded=person_reminded, content=content
        )

    # assertions
    data_reminders = data_model.get_response(ReminderEntity)
    assert len(list(data_reminders)) == 0


def test_get_started_complex4a():
    """
    Show me the traffic to each Whole Food branch in a 10 miles radius.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location1 = Location(
        text="each Whole Food branch in a 10 miles radius", value="Whole Food #1"
    )
    data_model.append(data_location1)
    data_location2 = Location(
        text="each Whole Food branch in a 10 miles radius", value="Whole Food #2"
    )
    data_model.append(data_location2)
    data_location3 = Location(
        text="each Whole Food branch in a 10 miles radius", value="Whole Food #3"
    )
    data_model.append(data_location3)
    data_location4 = Location(
        text="Whole Food branch in over a 10 miles radius", value="Whole Food #4"
    )
    data_model.append(data_location4)
    data_model.append(NavigationTrafficInfoEntity(destination=data_location1))
    data_model.append(NavigationTrafficInfoEntity(destination=data_location2))
    data_model.append(NavigationTrafficInfoEntity(destination=data_location3))
    data_model.append(NavigationTrafficInfoEntity(destination=data_location4))

    # code block to be tested
    destinations = Location.resolve_many_from_text(
        "each Whole Food branch in a 10 miles radius"
    )
    results = []
    for destination in destinations:
        traffic_info = Navigation.find_traffic_info(destination=destination)
        if traffic_info:
            results += traffic_info
    Responder.respond(response=results)

    # assertions
    data_traffic_infos_list = data_model.get_response([NavigationTrafficInfoEntity])
    assert len(list(data_traffic_infos_list)) == 1
    data_traffic_infos = data_traffic_infos_list[0]
    assert len(list(data_traffic_infos)) == 3


def test_get_started_complex4b():
    """
    Show me the traffic to each Whole Food branch in a 10 miles radius.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location1 = Location(
        text="each Whole Food branch in a 10 miles radius", value="Whole Food #1"
    )
    data_model.append(data_location1)
    data_location2 = Location(
        text="each Whole Food branch in a 10 miles radius", value="Whole Food #2"
    )
    data_model.append(data_location2)
    data_location3 = Location(
        text="each Whole Food branch in a 10 miles radius", value="Whole Food #3"
    )
    data_model.append(data_location3)
    data_location4 = Location(
        text="Whole Food branch in over a 10 miles radius", value="Whole Food #4"
    )
    data_model.append(data_location4)
    data_model.append(NavigationTrafficInfoEntity(destination=data_location1))
    data_model.append(NavigationTrafficInfoEntity(destination=data_location2))
    data_model.append(NavigationTrafficInfoEntity(destination=data_location4))

    # code block to be tested
    destinations = Location.resolve_many_from_text(
        "each Whole Food branch in a 10 miles radius"
    )
    response = []
    for destination in destinations:
        traffic_info = Navigation.find_traffic_info(destination=destination)
        response += traffic_info
    Responder.respond(response=response)

    # assertions
    data_traffic_infos_lists = data_model.get_response([NavigationTrafficInfoEntity])
    assert len(data_traffic_infos_lists) == 1
    data_traffic_infos = data_traffic_infos_lists[0]
    assert len(list(data_traffic_infos)) == 2
