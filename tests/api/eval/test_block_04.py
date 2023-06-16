from entities.generic import *
from entities.calendar import *
from entities.home import *
from entities.map import *
from entities.message import *
from entities.music import *
from entities.navigation import *
from entities.reminder import *
from entities.shopping import *
from entities.weather import *
from actions.calendar import *
from actions.clock import *
from actions.calendar import *
from actions.home import *
from actions.map import *
from actions.messages import *
from actions.music import *
from actions.navigation import *
from actions.reminders import *
from actions.responder import *
from actions.shopping import *
from actions.weather import *
from providers.data_model import DataModel
from datetime import datetime, timedelta
import utils.api_utils as utils
from utils.test_utils import (
    assert_equal,
    assert_not_equal,
    assert_true,
    assert_false,
    response_assertions,
    assert_test,
    entity_assertions,
)


def test_78_a():
    """
    If I get a text message from my boss Tony, then check my mail to see if I have any emails from work.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="a text message")
    data_model.append(data_message_content_type)
    data_sender_boss = Contact(text="my boss Tony")
    data_model.append(data_sender_boss)
    data_sender_work1 = Contact(text="work", value="worker 1")
    data_model.append(data_sender_work1)
    data_sender_work2 = Contact(text="work", value="worker 2")
    data_model.append(data_sender_work2)
    data_message = MessageEntity(
        message_content_type=data_message_content_type, sender=data_sender_boss
    )
    data_model.append(data_message)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type_email = MessageContentType(text="any emails")
    data_model.append(data_message_content_type_email)
    data_message2 = MessageEntity(
        sender=data_sender_work1,
        recipient=data_recipient,
        message_content_type=data_message_content_type_email,
    )
    data_model.append(data_message2)
    data_message3 = MessageEntity(
        sender=data_sender_work2,
        recipient=data_recipient,
        message_content_type=data_message_content_type_email,
    )
    data_model.append(data_message3)

    # start code block to test
    message_content_type = MessageContentType(text="a text message")
    sender = Contact(text="my boss Tony")
    messages = Messages.find_messages(
        sender=sender, message_content_type=message_content_type
    )
    test_messages = bool(messages)
    if test_messages:
        senders = Contact.resolve_many_from_text(text="work")
        message_content_type = MessageContentType.resolve_from_text(text="any emails")
        messages = []
        for sender in senders:
            messages += Messages.find_messages(
                sender=sender, message_content_type=message_content_type
            )
        Responder.respond(response=messages)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([MessageEntity]))
    actual = next(iterator, None)
    expected = [data_message2, data_message3]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_78_b():
    """
    If I get a text message from my boss Tony, then check my mail to see if I have any emails from work.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="a text message")
    data_model.append(data_message_content_type)
    data_sender_boss = Contact(text="my boss Tony")
    data_model.append(data_sender_boss)
    data_sender_work1 = Contact(text="work", value="worker 1")
    data_model.append(data_sender_work1)
    data_sender_work2 = Contact(text="work", value="worker 2")
    data_model.append(data_sender_work2)
    data_message = MessageEntity(
        message_content_type=data_message_content_type, sender=data_sender_work1
    )
    data_model.append(data_message)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type_email = MessageContentType(text="any emails")
    data_model.append(data_message_content_type_email)
    data_message2 = MessageEntity(
        sender=data_sender_work1,
        recipient=data_recipient,
        message_content_type=data_message_content_type,
    )
    data_model.append(data_message2)
    data_message3 = MessageEntity(
        sender=data_sender_work2,
        recipient=data_recipient,
        message_content_type=data_message_content_type,
    )
    data_model.append(data_message3)

    # start code block to test
    message_content_type = MessageContentType(text="a text message")
    sender = Contact(text="my boss Tony")
    messages = Messages.find_messages(
        sender=sender, message_content_type=message_content_type
    )
    test_messages = bool(messages)
    if test_messages:
        senders = Contact.resolve_many_from_text(text="work")
        message_content_type = MessageContentType.resolve_from_text(text="any emails")
        messages = []
        for sender in senders:
            messages += Messages.find_messages(
                sender=sender, message_content_type=message_content_type
            )
        Responder.respond(response=messages)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([MessageEntity]))
    actual = next(iterator, None)
    expected = []
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_79_a():
    """
    Check the weather for next tuesday and create a beach day event on my calendar if the temperature is above 90 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_tuesday = DateTime(
        text="next tuesday",
        value=datetime.now() + timedelta(days=((7 + 1 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_tuesday)
    data_weather_temperature = WeatherTemperature(text="above 90 degrees")
    data_model.append(data_weather_temperature)
    data_weather_temperature_neg = WeatherTemperature(text="below 80")
    data_model.append(data_weather_temperature_neg)
    data_weather_forecast = WeatherForecastEntity(
        date_time=data_date_time_tuesday, weather_temperature=data_weather_temperature
    )
    data_model.append(data_weather_forecast)
    data_event_name = EventName(text="beach day")
    data_model.append(data_event_name)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)

    # start code block to test
    date_time = DateTime.resolve_from_text("next tuesday")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    weather_temperature = WeatherTemperature.resolve_from_text("above 90 degrees")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_temperature=weather_temperature
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        event_name = EventName.resolve_from_text("beach day")
        event_calendar = EventCalendar.resolve_from_text("my calendar")
        Calendar.schedule_event(event_name=event_name, event_calendar=event_calendar)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(EventEntity)
    expected = [{"event_name": data_event_name, "event_calendar": data_event_calendar}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_79_b():
    """
    Check the weather for next tuesday and create a beach day event on my calendar if the temperature is above 90 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_tuesday = DateTime(
        text="next tuesday",
        value=datetime.now() + timedelta(days=((7 + 1 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_tuesday)
    data_weather_temperature = WeatherTemperature(text="above 90 degrees")
    data_model.append(data_weather_temperature)
    data_weather_temperature_neg = WeatherTemperature(text="below 80")
    data_model.append(data_weather_temperature_neg)
    data_weather_forecast = WeatherForecastEntity(
        date_time=data_date_time_tuesday,
        weather_temperature=data_weather_temperature_neg,
    )
    data_model.append(data_weather_forecast)
    data_event_name = EventName(text="beach day")
    data_model.append(data_event_name)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)

    # start code block to test
    date_time = DateTime.resolve_from_text("next tuesday")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    weather_temperature = WeatherTemperature.resolve_from_text("above 90 degrees")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_temperature=weather_temperature
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        event_name = EventName.resolve_from_text("beach day")
        event_calendar = EventCalendar.resolve_from_text("my calendar")
        Calendar.schedule_event(event_name=event_name, event_calendar=event_calendar)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(EventEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_80():
    """
    Message my brother I will not be able to make it to his house for dinner because of a flat tire, also look up tire repair places nearby.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="message")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="my brother")
    data_model.append(data_recipient)
    data_content = Content(
        text="I will not be able to make it to his house for dinner because of a flat tire"
    )
    data_model.append(data_content)

    data_location1 = Location(text="tire repair places", nearby=12)
    data_model.append(data_location1)
    data_location2 = Location(text="tire repair places", nearby=11)
    data_model.append(data_location2)
    data_location3 = Location(text="tire repair places", nearby=10)
    data_model.append(data_location3)
    data_map_entity1 = MapEntity(location=data_location1)
    data_model.append(data_map_entity1)
    data_map_entity2 = MapEntity(location=data_location2)
    data_model.append(data_map_entity2)
    data_map_entity3 = MapEntity(location=data_location3)
    data_model.append(data_map_entity3)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("message")
    recipient = Contact.resolve_from_text("my brother")
    content = Content.resolve_from_text(
        "I will not be able to make it to his house for dinner because of a flat tire"
    )
    Messages.send_message(
        message_content_type=message_content_type, recipient=recipient, content=content
    )

    locations = Location.resolve_many_from_text("tire repair places")
    locations = utils.sort(locations, "nearby")
    location = utils.first(locations)
    places = Map.find_on_map(location=location)
    Responder.respond(response=places)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "message_content_type": data_message_content_type,
        }
    ]
    entity_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([MapEntity]))
    actual = next(iterator, None)
    expected = [data_map_entity3]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_81():
    """
    Set a timer for 3:00 PM then enable home security alarm system to stay on until 8:00 PM
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_3pm = DateTime(
        text="3:00 PM",
        value=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time_3pm)
    data_home_device_action = HomeDeviceAction(text="enable")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="home security alarm")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="stay on")
    data_model.append(data_home_device_value)
    data_date_time_8pm = DateTime(
        text="until 8:00 PM",
        value=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time_8pm)

    # start code block to test
    date_time = DateTime.resolve_from_text("3:00 PM")
    Timer.create_timer(date_time=date_time)

    device_action = HomeDeviceAction.resolve_from_text("enable")
    device_name = HomeDeviceName.resolve_from_text("home security alarm")
    device_value = HomeDeviceValue.resolve_from_text("stay on")
    date_time = DateTime.resolve_from_text("until 8:00 PM")
    SmartHome.execute_home_device_action(
        device_action=device_action,
        device_name=device_name,
        device_value=device_value,
        date_time=date_time,
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(TimerEntity)
    expected = [{"date_time": data_date_time_3pm}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_action": data_home_device_action,
            "device_name": data_home_device_name,
            "device_value": data_home_device_value,
            "date_time": data_date_time_8pm,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_85_a():
    """
    If it starts raining between 3pm-5pm, turn the thermostat up to 73 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(
        text="between 3pm-5pm",
        value=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time
        )
    )
    data_home_device_action = HomeDeviceAction(text="turn")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="up tp 73 degrees")
    data_model.append(data_home_device_value)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    date_time = DateTime.resolve_from_text("between 3pm-5pm")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        device_action = HomeDeviceAction.resolve_from_text("turn")
        device_name = HomeDeviceName.resolve_from_text("the thermostat")
        device_value = HomeDeviceValue.resolve_from_text("up tp 73 degrees")
        SmartHome.execute_home_device_action(
            device_action=device_action,
            device_name=device_name,
            device_value=device_value,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_action": data_home_device_action,
            "device_name": data_home_device_name,
            "device_value": data_home_device_value,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_85_b():
    """
    If it starts raining between 3pm-5pm, turn the thermostat up to 73 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(
        text="between 3pm-5pm",
        value=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg, date_time=data_date_time
        )
    )
    data_home_device_action = HomeDeviceAction(text="turn")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="up tp 73 degrees")
    data_model.append(data_home_device_value)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    date_time = DateTime.resolve_from_text("between 3pm-5pm")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        device_action = HomeDeviceAction.resolve_from_text("turn")
        device_name = HomeDeviceName.resolve_from_text("the thermostat")
        device_value = HomeDeviceValue.resolve_from_text("up tp 73 degrees")
        SmartHome.execute_home_device_action(
            device_action=device_action,
            device_name=device_name,
            device_value=device_value,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(HomeDeviceEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_86():
    """
    Show me a map of downtown Phoenix and give me directions to the airport.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="downtown Phoenix")
    data_model.append(data_location)
    data_place = MapEntity(location=data_location)
    data_model.append(data_place)
    data_destination = Location(text="airport")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)

    # start code block to test
    location = Location.resolve_from_text("downtown Phoenix")
    places = Map.find_on_map(location=location)
    Responder.respond(response=places)

    destination = Location.resolve_from_text("to the airport")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([MapEntity]))
    actual = next(iterator, None)
    expected = [data_place]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_87():
    """
    Play my lofi Spotify playlist and buy tickets to the upcoming Joji show.
    """
    # test data
    data_model = DataModel(reset=True)
    data_playlist = Playlist(text="my lofi Spotify playlist")
    data_model.append(data_playlist)
    data_event_name = EventName(text="the upcoming Joji show")
    data_model.append(data_event_name)

    # start code block to test
    playlist = Playlist.resolve_from_text("my lofi Spotify playlist")
    Music.play_music(playlist=playlist)

    event_name = EventName.resolve_from_text("the upcoming Joji show")
    Calendar.purchase_tickets(event_name=event_name)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MusicEntity)
    expected = [{"playlist": data_playlist}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(EventTicketEntity)
    expected = [{"event_name": data_event_name}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_88_a():
    """
    Check if it's supposed to rain tonight and if it's not text Brian that I want to go out tonight
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(text="tonight")
    data_model.append(data_date_time)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute_neg, date_time=data_date_time
    )
    data_model.append(data_weather_forecast)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_contact_brian = Contact(text="Brian")
    data_model.append(data_contact_brian)
    data_content = Content(text="I want to go out tonight")
    data_model.append(data_content)

    # start code block to test
    data_weather_attribute = WeatherAttribute.resolve_from_text("rain")
    date_time = DateTime.resolve_from_text("tonight")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=data_weather_attribute
    )
    Responder.respond(response=weather_forecasts)

    test_weather_forecasts = bool(weather_forecasts)
    if not test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("text")
        recipient = Contact.resolve_from_text("Brian")
        content = Content.resolve_from_text("I want to go out tonight")
        Messages.send_message(
            message_content_type=message_content_type,
            recipient=recipient,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = []
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "message_content_type": data_message_content_type,
            "recipient": data_contact_brian,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_88_b():
    """
    Check if it's supposed to rain tonight and if it's not text Brian that I want to go out tonight
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(text="tonight")
    data_model.append(data_date_time)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute, date_time=data_date_time
    )
    data_model.append(data_weather_forecast)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_contact_brian = Contact(text="Brian")
    data_model.append(data_contact_brian)
    data_content = Content(text="I want to go out tonight")
    data_model.append(data_content)

    # start code block to test
    data_weather_attribute = WeatherAttribute.resolve_from_text("rain")
    date_time = DateTime.resolve_from_text("tonight")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=data_weather_attribute
    )
    Responder.respond(response=weather_forecasts)

    test_weather_forecasts = bool(weather_forecasts)
    if not test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("text")
        recipient = Contact.resolve_from_text("Brian")
        content = Content.resolve_from_text("I want to go out tonight")
        Messages.send_message(
            message_content_type=message_content_type,
            recipient=recipient,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_92():
    """
    Look up free events for this weekend and let me know what the weather will be.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name1 = EventName(text="free events", value="art show")
    data_model.append(data_event_name1)
    data_event_name2 = EventName(text="free events", value="community event")
    data_model.append(data_event_name2)
    data_date_time1 = DateTime(
        text="this weekend", value=datetime.now() + timedelta(days=0)
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="this weekend", value=datetime.now() + timedelta(days=0)
    )
    data_model.append(data_date_time2)
    data_model.append(
        data_event1 := EventEntity(
            event_name=data_event_name1, date_time=data_date_time1
        )
    )
    data_model.append(
        data_event2 := EventEntity(
            event_name=data_event_name1, date_time=data_date_time2
        )
    )
    data_model.append(
        data_event3 := EventEntity(
            event_name=data_event_name2, date_time=data_date_time2
        )
    )
    data_model.append(
        data_weather_forecast1 := WeatherForecastEntity(date_time=data_date_time1)
    )
    data_model.append(
        data_weather_forecast2 := WeatherForecastEntity(date_time=data_date_time2)
    )

    # start code block to test
    event_names = EventName.resolve_many_from_text("free events")
    date_times = DateTime.resolve_many_from_text("this weekend")
    events = []
    for event_name in event_names:
        for date_time in date_times:
            events += Calendar.find_events(event_name=event_name, date_time=date_time)
    Responder.respond(response=events)

    weather_forecasts = Weather.find_weather_forecasts()
    Responder.respond(response=weather_forecasts)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event1, data_event2, data_event3]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast1, data_weather_forecast2]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_94():
    """
    When rain is forecasted for tomorrow? remind me at 9pm the night before to put out Quinten's boots by the front door.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_model.append(data_weather_attribute_neg)
    data_date_time_tomorrow = DateTime(
        text="tomorrow",
    )
    data_model.append(data_date_time_tomorrow)
    data_model.append(
        data_weather_forecast1 := WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time_tomorrow
        )
    )
    data_model.append(
        data_weather_forecast2 := WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg,
            date_time=data_date_time_tomorrow,
        )
    )
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time_9pm = DateTime(
        text="9pm the night before",
    )
    data_model.append(data_date_time_9pm)
    data_content = Content(text="put out Quinten's boots by the front door")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("rain")
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time
    )
    Responder.respond(response=weather_forecasts)

    person_reminded = Contact.resolve_from_text("me")
    date_time = DateTime.resolve_from_text("at 9pm the night before")
    content = Content.resolve_from_text("put out Quinten's boots by the front door")
    Reminders.create_reminder(
        person_reminded=person_reminded, date_time=date_time, content=content
    )
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast1]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_time_9pm,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_96():
    """
    Add almond milk, pomegranate seeds, and granola to my shopping list and set a reminder for Saturday morning at 9am that I need to be home from the store by noon.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name1 = ProductName(
        text="almond milk, pomegranate seeds, and granola", value="almond milk"
    )
    data_model.append(data_product_name1)
    data_product_name2 = ProductName(
        text="almond milk, pomegranate seeds, and granola", value="pomegranate seeds"
    )
    data_model.append(data_product_name2)
    data_product_name3 = ProductName(
        text="almond milk, pomegranate seeds, and granola", value="granola"
    )
    data_model.append(data_product_name3)
    data_shopping_list_name = ShoppingListName(text="my shopping list")
    data_model.append(data_shopping_list_name)
    data_date_time = DateTime(text="Saturday morning at 9am")
    data_model.append(data_date_time)
    data_content = Content(text="I need to be home from the store by noon")
    data_model.append(data_content)

    # start code block to test
    product_names = ProductName.resolve_many_from_text(
        "almond milk, pomegranate seeds, and granola"
    )
    shopping_list_name = ShoppingListName.resolve_from_text("my shopping list")
    for product_name in product_names:
        Shopping.add_to_shopping_list(
            product_name=product_name, shopping_list_name=shopping_list_name
        )

    date_time = DateTime.resolve_from_text("Saturday morning at 9am")
    content = Content.resolve_from_text("I need to be home from the store by noon")
    Reminders.create_reminder(date_time=date_time, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ShoppingListEntity)
    expected = [
        {
            "product_name": data_product_name,
            "shopping_list_name": data_shopping_list_name,
        }
        for data_product_name in [
            data_product_name1,
            data_product_name2,
            data_product_name3,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": data_date_time,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_98():
    """
    Check my calendar for this weekend and message Ashley to invite her to lunch for whichever day I have free time in the afternoon.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)
    data_date_time1 = DateTime(text="this weekend", value="Saturday")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="this weekend", value="Sunday")
    data_model.append(data_date_time2)
    data_event1 = EventEntity(
        event_calendar=data_event_calendar, date_time=data_date_time1
    )
    data_model.append(data_event1)
    data_event2 = EventEntity(
        event_calendar=data_event_calendar, date_time=data_date_time2
    )
    data_model.append(data_event2)
    data_recipient = Contact(text="Ashley")
    data_model.append(data_recipient)
    data_content = Content(
        text="invite her to lunch for whichever day I have free time in the afternoon"
    )
    data_model.append(data_content)

    # start code block to test
    event_calendar = EventCalendar.resolve_from_text("my calendar")
    date_times = DateTime.resolve_many_from_text("this weekend")
    events = []
    for date_time in date_times:
        events += Calendar.find_events(
            event_calendar=event_calendar, date_time=date_time
        )
    Responder.respond(response=events)

    recipient = Contact.resolve_from_text("Ashley")
    content = Content.resolve_from_text(
        "invite her to lunch for whichever day I have free time in the afternoon"
    )
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event1, data_event2]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_99():
    """
    Go shopping and buy multiples of items on my shopping list and prompt me after you buy it, as well as set a reminder of the time it will be delivered.
    """
    # test data
    data_model = DataModel(reset=True)
    data_shopping_list_name = ShoppingListName(text="my shopping list")
    data_model.append(data_shopping_list_name)

    # start code block to test
    shopping_list_name = ShoppingListName.resolve_from_text("my shopping list")
    order = Shopping.order(shopping_list_name=shopping_list_name)
    Responder.respond(response=order)

    date_time = DateTime.resolve_from_entity(order)
    Reminders.create_reminder(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response(OrderEntity))
    actual = next(iterator, None)
    expected = OrderEntity(shopping_list_name=data_shopping_list_name)
    response_assertions([expected], [actual], test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": DateTime(value=order),
        }
        for order in data_model.get_data(OrderEntity)
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_102():
    """
    Set an alarm for 7:30am and notify me with a reminder 2 hours later that I need to message Vincent with an update on our work project.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="7:30am")
    data_model.append(data_date_time)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time2 = DateTime(text="2 hours later")
    data_model.append(data_date_time2)
    data_content = Content(
        text="I need to message Vincent with an update on our work project"
    )
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("7:30am")
    Alarm.create_alarm(date_time=date_time)

    person_reminded = Contact.resolve_from_text("me")
    date_time = DateTime.resolve_from_text("2 hours later")
    content = Content.resolve_from_text(
        "I need to message Vincent with an update on our work project"
    )
    Reminders.create_reminder(
        person_reminded=person_reminded, date_time=date_time, content=content
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [{"date_time": data_date_time}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_time2,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_104_a():
    """
    In the event that Jessica messages with road closure information downtown, create a 3pm alarm, so I can leave earlier.
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender = Contact(text="Jessica")
    data_model.append(data_sender)
    data_content = Content(text="road closure information downtown")
    data_model.append(data_content)
    data_content_neg = Content(text="all roads are clear")
    data_model.append(data_content_neg)
    data_date_time = DateTime(text="3pm")
    data_model.append(data_date_time)
    data_message = MessageEntity(sender=data_sender, content=data_content)
    data_model.append(data_message)

    # start code block to test
    sender = Contact.resolve_from_text("Jessica")
    content = Content.resolve_from_text("road closure information downtown")
    messages = Messages.find_messages(sender=sender, content=content)
    test_messages = bool(messages)
    if test_messages:
        date_time = DateTime.resolve_from_text("3pm")
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [{"date_time": data_date_time}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_104_b():
    """
    In the event that Jessica messages with road closure information downtown, create a 3pm alarm, so I can leave earlier.
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender = Contact(text="Jessica")
    data_model.append(data_sender)
    data_content = Content(text="road closure information downtown")
    data_model.append(data_content)
    data_content_neg = Content(text="all roads are clear")
    data_model.append(data_content_neg)
    data_date_time = DateTime(text="3pm")
    data_model.append(data_date_time)
    data_message = MessageEntity(sender=data_sender, content=data_content_neg)
    data_model.append(data_message)

    # start code block to test
    sender = Contact.resolve_from_text("Jessica")
    content = Content.resolve_from_text("road closure information downtown")
    messages = Messages.find_messages(sender=sender, content=content)
    test_messages = bool(messages)
    if test_messages:
        date_time = DateTime.resolve_from_text("3pm")
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_105():
    """
    Order tickets for the art festival this weekend and add the address to my navigation.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="the art festival")
    data_model.append(data_event_name)
    data_date_time1 = DateTime(text="this weekend", value="Saturday")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="this weekend", value="Sunday")
    data_model.append(data_date_time2)
    data_event1 = EventEntity(event_name=data_event_name, date_time=data_date_time1)
    data_model.append(data_event1)
    data_event2 = EventEntity(event_name=data_event_name, date_time=data_date_time2)
    data_model.append(data_event2)
    data_destination1 = Location(value=data_event1)
    data_model.append(data_destination1)
    data_destination2 = Location(value=data_event2)
    data_model.append(data_destination2)
    data_navigation_direction1 = NavigationDirectionEntity(
        destination=data_destination1
    )
    data_model.append(data_navigation_direction1)
    data_navigation_direction2 = NavigationDirectionEntity(
        destination=data_destination2
    )
    data_model.append(data_navigation_direction2)

    # start code block to test
    event_name = EventName.resolve_from_text("the art festival")
    date_times = DateTime.resolve_many_from_text("this weekend")
    for date_time in date_times:
        Calendar.purchase_tickets(event_name=event_name, date_time=date_time)

    events = Calendar.find_events(event_name=event_name)
    navigation_directions = []
    for event in events:
        destination = Location.resolve_from_entity(event)
        navigation_directions += Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventTicketEntity)
    expected = [
        {"event_name": data_event_name, "date_time": data_date_time}
        for data_date_time in [data_date_time1, data_date_time2]
    ]
    entity_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction1, data_navigation_direction2]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_108():
    """
    The temperature at home should be set to 82 degrees after texting Bob about picking the kids up from soccer practice.
    """
    # test data
    data_model = DataModel(reset=True)
    data_device_name = HomeDeviceName(text="The temperature at home")
    data_model.append(data_device_name)
    data_device_action = HomeDeviceAction(text="set")
    data_model.append(data_device_action)
    data_device_value = HomeDeviceValue(text="82 degrees")
    data_model.append(data_device_value)
    data_recipient = Contact(text="Bob")
    data_model.append(data_recipient)
    data_content = Content(text="picking the kids up from soccer practice")
    data_model.append(data_content)

    # start code block to test
    recipient = Contact.resolve_from_text("Bob")
    content = Content.resolve_from_text("picking the kids up from soccer practice")
    Messages.send_message(recipient=recipient, content=content)

    device_name = HomeDeviceName.resolve_from_text("The temperature at home")
    device_action = HomeDeviceAction.resolve_from_text("set")
    device_value = HomeDeviceValue.resolve_from_text("82 degrees")
    SmartHome.execute_home_device_action(
        device_name=device_name, device_action=device_action, device_value=device_value
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_name": data_device_name,
            "device_action": data_device_action,
            "device_value": data_device_value,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_109_a():
    """
    Send an email to manager Steve after I get a text confirmation for the meeting from Jennie.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="an email")
    data_model.append(data_message_content_type)
    data_recipient_steve = Contact(text="manager Steve")
    data_model.append(data_recipient_steve)
    data_recipient_i = Contact(text="I")
    data_model.append(data_recipient_i)
    data_content = Content(text="a text confirmation for the meeting")
    data_model.append(data_content)
    data_content_neg = Content(text="cannot attend")
    data_model.append(data_content_neg)
    data_sender = Contact(text="Jennie")
    data_model.append(data_sender)
    data_message = MessageEntity(
        sender=data_sender, content=data_content, recipient=data_recipient_i
    )
    data_model.append(data_message)

    # start code block to test
    recipient = Contact.resolve_from_text("I")
    content = Content.resolve_from_text("a text confirmation for the meeting")
    sender = Contact.resolve_from_text("Jennie")
    messages = Messages.find_messages(
        recipient=recipient, sender=sender, content=content
    )
    test_messages = bool(messages)
    if test_messages:
        message_content_type = MessageContentType.resolve_from_text("an email")
        recipient = Contact.resolve_from_text("manager Steve")
        Messages.send_message(
            recipient=recipient, message_content_type=message_content_type
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient_i,
            "content": data_content,
            "sender": data_sender,
        },
        {
            "message_content_type": data_message_content_type,
            "message_content_type": data_message_content_type,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_109_b():
    """
    Send an email to manager Steve after I get a text confirmation for the meeting from Jennie.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="an email")
    data_model.append(data_message_content_type)
    data_recipient_steve = Contact(text="manager Steve")
    data_model.append(data_recipient_steve)
    data_recipient_i = Contact(text="I")
    data_model.append(data_recipient_i)
    data_content = Content(text="a text confirmation for the meeting")
    data_model.append(data_content)
    data_content_neg = Content(text="cannot attend")
    data_model.append(data_content_neg)
    data_sender = Contact(text="Jennie")
    data_model.append(data_sender)
    data_message = MessageEntity(
        sender=data_sender, content=data_content_neg, recipient=data_recipient_i
    )
    data_model.append(data_message)

    # start code block to test
    recipient = Contact.resolve_from_text("I")
    content = Content.resolve_from_text("a text confirmation for the meeting")
    sender = Contact.resolve_from_text("Jennie")
    messages = Messages.find_messages(
        recipient=recipient, sender=sender, content=content
    )
    test_messages = bool(messages)
    if test_messages:
        message_content_type = MessageContentType.resolve_from_text("an email")
        recipient = Contact.resolve_from_text("manager Steve")
        Messages.send_message(
            recipient=recipient, message_content_type=message_content_type
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient_i,
            "content": data_content_neg,
            "sender": data_sender,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_112_a():
    """
    In the case that I receive an email from Kaiser Permanente, remind me to read it after 10 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type = MessageContentType(text="an email")
    data_model.append(data_message_content_type)
    data_message_content_type_neg = MessageContentType(text="an email")
    data_model.append(data_message_content_type_neg)
    data_sender = Contact(text="Kaiser Permanente")
    data_model.append(data_sender)
    data_message = MessageEntity(
        recipient=data_recipient,
        sender=data_sender,
        message_content_type=data_message_content_type,
    )
    data_model.append(data_message)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="read it")
    data_model.append(data_content)
    data_date_time = DateTime(text="after 10 minutes")
    data_model.append(data_date_time)

    # start code block to test
    recipient = Contact.resolve_from_text("I")
    message_content_type = MessageContentType.resolve_from_text("an email")
    sender = Contact.resolve_from_text("Kaiser Permanente")
    messages = Messages.find_messages(
        recipient=recipient, sender=sender, message_content_type=message_content_type
    )
    test_messages = bool(messages)
    if test_messages:
        person_reminded = Contact.resolve_from_text("me")
        content = Content.resolve_from_text("read it")
        date_time = DateTime.resolve_from_text("after 10 minutes")
        Reminders.create_reminder(
            person_reminded=person_reminded, content=content, date_time=date_time
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)[-1:]
    expected = [
        {
            "person_reminded": data_person_reminded,
            "content": data_content,
            "date_time": data_date_time,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_112_b():
    """
    In the case that I receive an email from Kaiser Permanente, remind me to read it after 10 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type = MessageContentType(text="an email")
    data_model.append(data_message_content_type)
    data_message_content_type_neg = MessageContentType(text="a text")
    data_model.append(data_message_content_type_neg)
    data_sender = Contact(text="Kaiser Permanente")
    data_model.append(data_sender)
    data_message = MessageEntity(
        recipient=data_recipient,
        sender=data_sender,
        message_content_type=data_message_content_type_neg,
    )
    data_model.append(data_message)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="read it")
    data_model.append(data_content)
    data_date_time = DateTime(text="after 10 minutes")
    data_model.append(data_date_time)

    # start code block to test
    recipient = Contact.resolve_from_text("I")
    message_content_type = MessageContentType.resolve_from_text("an email")
    sender = Contact.resolve_from_text("Kaiser Permanente")
    messages = Messages.find_messages(
        recipient=recipient, sender=sender, message_content_type=message_content_type
    )
    test_messages = bool(messages)
    if test_messages:
        person_reminded = Contact.resolve_from_text("me")
        content = Content.resolve_from_text("read it")
        date_time = DateTime.resolve_from_text("after 10 minutes")
        Reminders.create_reminder(
            person_reminded=person_reminded, content=content, date_time=date_time
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_113():
    """
    On the 2nd of November set a reminder that I will be going out with friends and to remind me every 3 days before the event.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="On the 2nd of November")
    data_model.append(data_date_time)
    data_content = Content(text="I will be going out with friends")
    data_model.append(data_content)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_times1 = DateTime(text="every 3 days before the event", value="day 1")
    data_model.append(data_date_times1)
    data_date_times2 = DateTime(text="every 3 days before the event", value="day 2")
    data_model.append(data_date_times2)

    # start code block to test
    date_time = DateTime.resolve_from_text("On the 2nd of November")
    content = Content.resolve_from_text("I will be going out with friends")
    Reminders.create_reminder(date_time=date_time, content=content)

    person_reminded = Contact.resolve_from_text("me")
    date_times = DateTime.resolve_many_from_text("every 3 days before the event")
    for date_time in date_times:
        Reminders.create_reminder(person_reminded=person_reminded, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": data_date_time,
            "content": data_content,
        },
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_times1,
        },
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_times2,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_118_a():
    """
    In the case that the rain projection is above 90%, text my golf group and say that I am going to today's game.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain projection is above 90%")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="hot and sunny")
    data_model.append(data_weather_attribute_neg)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_recipient1 = Contact(text="my golf group", value="Joe")
    data_model.append(data_recipient1)
    data_recipient2 = Contact(text="my golf group", value="Brian")
    data_model.append(data_recipient2)
    data_content = Content(text="I am going to today's game")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text(
        "rain projection is above 90%"
    )
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("text")
        recipients = Contact.resolve_many_from_text("my golf group")
        content = Content.resolve_from_text("I am going to today's game")
        for recipient in recipients:
            Messages.send_message(
                recipient=recipient,
                content=content,
                message_content_type=message_content_type,
            )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "message_content_type": data_message_content_type,
        }
        for data_recipient in [data_recipient1, data_recipient2]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_118_b():
    """
    In the case that the rain projection is above 90%, text my golf group and say that I am going to today's game.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain projection is above 90%")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="hot and sunny")
    data_model.append(data_weather_attribute_neg)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute_neg
    )
    data_model.append(data_weather_forecast)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_recipient1 = Contact(text="my golf group", value="Joe")
    data_model.append(data_recipient1)
    data_recipient2 = Contact(text="my golf group", value="Brian")
    data_model.append(data_recipient2)
    data_content = Content(text="I am going to today's game")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text(
        "rain projection is above 90%"
    )
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("text")
        recipients = Contact.resolve_many_from_text("my golf group")
        content = Content.resolve_from_text("I am going to today's game")
        for recipient in recipients:
            Messages.send_message(
                recipient=recipient,
                content=content,
                message_content_type=message_content_type,
            )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_121():
    """
    Remind me to buy apples, dates, and cheese at the grocery store, and also remind me to text Nathan about Grandma's birthday party.
    """
    # test data
    data_model = DataModel(reset=True)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content1 = Content(text="buy apples, dates, and cheese at the grocery store")
    data_model.append(data_content1)
    data_content2 = Content(text="text Nathan about Grandma's birthday party")
    data_model.append(data_content2)

    # start code block to test
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text(
        "buy apples, dates, and cheese at the grocery store"
    )
    Reminders.create_reminder(person_reminded=person_reminded, content=content)

    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("text Nathan about Grandma's birthday party")
    Reminders.create_reminder(person_reminded=person_reminded, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {"person_reminded": data_person_reminded, "content": data_content1},
        {"person_reminded": data_person_reminded, "content": data_content2},
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_124_a():
    """
    Check for potential snowfall this weekend in Denver, and should the forecast say we're getting at least 6 inches, email Jason to invite him to go snowboarding.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="snowfall")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(text="this weekend")
    data_model.append(data_date_time)
    data_location = Location(text="in Denver")
    data_model.append(data_location)
    data_weather = WeatherForecastEntity(
        date_time=data_date_time,
        location=data_location,
        weather_attribute=data_weather_attribute,
    )
    data_model.append(data_weather)
    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Jason")
    data_model.append(data_recipient)
    data_content = Content(text="invite him to go snowboarding")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("snowfall")
    date_time = DateTime.resolve_from_text("this weekend")
    location = Location.resolve_from_text("in Denver")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time, location=location
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("email")
        recipient = Contact.resolve_from_text("Jason")
        content = Content.resolve_from_text("invite him to go snowboarding")
        Messages.send_message(
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "message_content_type": data_message_content_type,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_124_b():
    """
    Check for potential snowfall this weekend in Denver, and should the forecast say we're getting at least 6 inches, email Jason to invite him to go snowboarding.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="snowfall")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(text="this weekend")
    data_model.append(data_date_time)
    data_location = Location(text="in Denver")
    data_model.append(data_location)
    data_weather = WeatherForecastEntity(
        date_time=data_date_time,
        location=data_location,
        weather_attribute=data_weather_attribute_neg,
    )
    data_model.append(data_weather)
    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Jason")
    data_model.append(data_recipient)
    data_content = Content(text="invite him to go snowboarding")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("snowfall")
    date_time = DateTime.resolve_from_text("this weekend")
    location = Location.resolve_from_text("in Denver")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time, location=location
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("email")
        recipient = Contact.resolve_from_text("Jason")
        content = Content.resolve_from_text("invite him to go snowboarding")
        Messages.send_message(
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_126():
    """
    Add a bikram yoga class to my calendar Saturday at 9am and set an alarm for 7am for that same morning.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="a bikram yoga class")
    data_model.append(data_event_name)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)
    data_date_time = DateTime(text="Saturday at 9am")
    data_model.append(data_date_time)
    data_date_time_alarm = DateTime(text="7am for that same morning")
    data_model.append(data_date_time_alarm)

    # start code block to test
    event_name = EventName.resolve_from_text("a bikram yoga class")
    event_calendar = EventCalendar.resolve_from_text("my calendar")
    date_time = DateTime.resolve_from_text("Saturday at 9am")
    Calendar.schedule_event(
        event_name=event_name, event_calendar=event_calendar, date_time=date_time
    )

    date_time = DateTime.resolve_from_text("7am for that same morning")
    Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventEntity)
    expected = [
        {
            "event_name": data_event_name,
            "event_calendar": data_event_calendar,
            "date_time": data_date_time,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(AlarmEntity)
    expected = [{"date_time": data_date_time_alarm}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_129():
    """
    Get directions to the party's address I have in my calendar and message Samantha to see what I should bring.
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination = Location(text="the party's address I have in my calendar")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)
    data_recipient = Contact(text="Samantha")
    data_model.append(data_recipient)
    data_content = Content(text="see what I should bring")
    data_model.append(data_content)

    # start code block to test
    destination = Location.resolve_from_text(
        "the party's address I have in my calendar"
    )
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(navigation_directions)

    recipient = Contact.resolve_from_text("Samantha")
    content = Content.resolve_from_text("see what I should bring")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_131():
    """
    Set an alarm for 6:30am this Tuesday, and make sure it repeats on Thursday and Saturday too.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="6:30am this Tuesday")
    data_model.append(data_date_time)
    data_date_time_repeat1 = DateTime(text="Thursday and Saturday", value="Thursday")
    data_model.append(data_date_time_repeat1)
    data_date_time_repeat2 = DateTime(text="Thursday and Saturday", value="Saturday")
    data_model.append(data_date_time_repeat2)

    # start code block to test
    date_time = DateTime.resolve_from_text("6:30am this Tuesday")
    Alarm.create_alarm(date_time=date_time)

    date_times = DateTime.resolve_many_from_text("Thursday and Saturday")
    for date_time in date_times:
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {"date_time": date_time}
        for date_time in [
            data_date_time,
            data_date_time_repeat1,
            data_date_time_repeat2,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_132():
    """
    Play my Intense Workout spotify playlist in the afternoon on Tuesday, Thursday, and Saturday.
    """
    # test data
    data_model = DataModel(reset=True)
    data_playlist = Playlist(text="my Intense Workout spotify playlist")
    data_model.append(data_playlist)
    data_date_time1 = DateTime(
        text="afternoon on Tuesday, Thursday, and Saturday", value="Tuesday"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="afternoon on Tuesday, Thursday, and Saturday", value="Thursday"
    )
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(
        text="afternoon on Tuesday, Thursday, and Saturday", value="Saturday"
    )
    data_model.append(data_date_time3)

    # start code block to test
    playlist = Playlist.resolve_from_text("my Intense Workout spotify playlist")
    date_times = DateTime.resolve_many_from_text(
        "afternoon on Tuesday, Thursday, and Saturday"
    )
    for date_time in date_times:
        Music.play_music(playlist=playlist, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MusicEntity)
    expected = [
        {"playlist": data_playlist, "date_time": date_time}
        for date_time in [
            data_date_time1,
            data_date_time2,
            data_date_time3,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_134():
    """
    Text everyone in my close friends group a photo of me at the ball game.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_recipient1 = Contact(text="everyone in my close friends group", value="John")
    data_model.append(data_recipient1)
    data_recipient2 = Contact(text="everyone in my close friends group", value="Henry")
    data_model.append(data_recipient2)
    data_content = Content(text="a photo of me at the ball game")
    data_model.append(data_content)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("text")
    recipients = Contact.resolve_many_from_text("everyone in my close friends group")
    content = Content.resolve_from_text("a photo of me at the ball game")
    for recipient in recipients:
        Messages.send_message(
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "message_content_type": data_message_content_type,
        }
        for data_recipient in [
            data_recipient1,
            data_recipient2,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_138():
    """
    Text everyone in my basketball group list that the referee fees increased by $3.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_recipient1 = Contact(text="everyone in my basketball group list", value="John")
    data_model.append(data_recipient1)
    data_recipient2 = Contact(
        text="everyone in my basketball group list", value="Henry"
    )
    data_model.append(data_recipient2)
    data_content = Content(text="the referee fees increased by $3")
    data_model.append(data_content)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("text")
    recipients = Contact.resolve_many_from_text("everyone in my close friends group")
    content = Content.resolve_from_text("the referee fees increased by $3")
    for recipient in recipients:
        Messages.send_message(
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "message_content_type": data_message_content_type,
        }
        for data_recipient in [
            data_recipient1,
            data_recipient2,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_139():
    """
    Add a visit to the lake to my calendar for January 2nd at 3:00 and remind me every day leading up to the day.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="a visit to the lake")
    data_model.append(data_event_name)
    data_date_time = DateTime(text="January 2nd at 3:00")
    data_model.append(data_date_time)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time_reminder1 = DateTime(
        text="every day leading up to the day", value="1"
    )
    data_model.append(data_date_time_reminder1)
    data_date_time_reminder2 = DateTime(
        text="every day leading up to the day", value="2"
    )
    data_model.append(data_date_time_reminder2)
    data_date_time_reminder3 = DateTime(
        text="every day leading up to the day", value="3"
    )
    data_model.append(data_date_time_reminder3)

    # start code block to test
    event_name = EventName.resolve_from_text("a visit to the lake")
    date_time = DateTime.resolve_from_text("January 2nd at 3:00")
    Calendar.schedule_event(date_time=date_time, event_name=event_name)

    person_reminded = Contact.resolve_from_text("me")
    date_time_reminders = DateTime.resolve_many_from_text(
        "every day leading up to the day"
    )
    for date_time_reminder in date_time_reminders:
        Reminders.create_reminder(
            person_reminded=person_reminded, date_time=date_time_reminder
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventEntity)
    expected = [
        {
            "date_time": data_date_time,
            "event_name": data_event_name,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "date_time": date_time,
        }
        for date_time in [
            data_date_time_reminder1,
            data_date_time_reminder2,
            data_date_time_reminder3,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_140_a():
    """
    Is there a Laker game on Monday, Wednesday, and Thursday?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="a Laker game")
    data_model.append(data_event_name)
    data_date_time1 = DateTime(
        text="on Monday, Wednesday, and Thursday", value="Monday"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="on Monday, Wednesday, and Thursday", value="Wednesday"
    )
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(
        text="on Monday, Wednesday, and Thursday", value="Thursday"
    )
    data_model.append(data_date_time3)
    data_event1 = EventEntity(event_name=data_event_name, date_time=data_date_time1)
    data_model.append(data_event1)
    data_event2 = EventEntity(event_name=data_event_name, date_time=data_date_time3)
    data_model.append(data_event2)

    # start code block to test
    event_name = EventName.resolve_from_text("a Laker game")
    date_times = DateTime.resolve_many_from_text("on Monday, Wednesday, and Thursday")
    events = []
    for date_time in date_times:
        events += Calendar.find_events(date_time=date_time, event_name=event_name)
    Responder.respond(response=events)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event1, data_event2]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_140_b():
    """
    Is there a Laker game on Monday, Wednesday, and Thursday?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="a Laker game")
    data_model.append(data_event_name)
    data_date_time1 = DateTime(
        text="on Monday, Wednesday, and Thursday", value="Monday"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="on Monday, Wednesday, and Thursday", value="Wednesday"
    )
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(
        text="on Monday, Wednesday, and Thursday", value="Thursday"
    )
    data_model.append(data_date_time3)
    data_date_time_neg = DateTime(text="Friday", value="Friday")
    data_model.append(data_date_time_neg)
    data_event1 = EventEntity(event_name=data_event_name, date_time=data_date_time_neg)
    data_model.append(data_event1)

    # start code block to test
    event_name = EventName.resolve_from_text("a Laker game")
    date_times = DateTime.resolve_many_from_text("on Monday, Wednesday, and Thursday")
    events = []
    for date_time in date_times:
        events += Calendar.find_events(date_time=date_time, event_name=event_name)
    Responder.respond(response=events)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = []
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_142():
    """
    Find directions to three closest Costco stores.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location1 = Location(text="to three Costco stores", closest="100")
    data_model.append(data_location1)
    data_location2 = Location(text="to three Costco stores", closest="120")
    data_model.append(data_location2)
    data_location3 = Location(text="to three Costco stores", closest="35")
    data_model.append(data_location3)
    data_location4 = Location(text="to three Costco stores", closest="2000")
    data_model.append(data_location4)
    data_location5 = Location(text="to three Costco stores", closest="80")
    data_model.append(data_location5)
    data_navigation_directions1 = NavigationDirectionEntity(destination=data_location1)
    data_model.append(data_navigation_directions1)
    data_navigation_directions2 = NavigationDirectionEntity(destination=data_location2)
    data_model.append(data_navigation_directions2)
    data_navigation_directions3 = NavigationDirectionEntity(destination=data_location3)
    data_model.append(data_navigation_directions3)
    data_navigation_directions4 = NavigationDirectionEntity(destination=data_location4)
    data_model.append(data_navigation_directions4)
    data_navigation_directions5 = NavigationDirectionEntity(destination=data_location5)
    data_model.append(data_navigation_directions5)

    # start code block to test
    destinations = Location.resolve_many_from_text("Costco stores")
    destinations = utils.sort(destinations, "closest")
    destinations = utils.first(destinations, 3)
    navigation_directions = []
    for destination in destinations:
        navigation_directions += Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [
        data_navigation_directions1,
        data_navigation_directions2,
        data_navigation_directions4,
    ]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_145():
    """
    Buy cauliflower and broccoli online at the grocery store and have them shipped every 15th of the month.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name1 = ProductName(
        text="cauliflower and broccoli", value="cauliflower"
    )
    data_model.append(data_product_name1)
    data_product_name2 = ProductName(text="cauliflower and broccoli", value="broccoli")
    data_model.append(data_product_name2)
    data_location = Location(text="the grocery store")
    data_model.append(data_location)
    data_date_time1 = DateTime(text="every 15th of the month", value="1/15")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="every 15th of the month", value="2/15")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="every 15th of the month", value="3/15")
    data_model.append(data_date_time3)

    # start code block to test
    product_names = ProductName.resolve_many_from_text("cauliflower and broccoli")
    location = Location.resolve_from_text("the grocery store")
    date_times = DateTime.resolve_many_from_text("every 15th of the month")
    for product_name in product_names:
        for date_time in date_times:
            Shopping.order(
                product_name=product_name, location=location, date_time=date_time
            )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(OrderEntity)
    expected = []
    for data_product_name in [data_product_name1, data_product_name2]:
        for data_date_time in [data_date_time1, data_date_time2, data_date_time3]:
            expected.append(
                {
                    "product_name": data_product_name,
                    "location": data_location,
                    "date_time": data_date_time,
                }
            )
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_146():
    """
    Set an alarm for every 3 hours starting at 2 am and stopping at 10 pm.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(text="every 3 hours starting at 2 am", value="2am")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="every 3 hours starting at 2 am", value="5am")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="every 3 hours starting at 2 am", value="8am")
    data_model.append(data_date_time3)
    data_date_time4 = DateTime(text="every 3 hours starting at 2 am", value="11am")
    data_model.append(data_date_time4)

    # start code block to test
    date_times = DateTime.resolve_many_from_text("every 3 hours starting at 2 am")
    for date_time in date_times:
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = []
    for data_date_time in [
        data_date_time1,
        data_date_time2,
        data_date_time3,
        data_date_time4,
    ]:
        expected.append(
            {
                "date_time": data_date_time,
            }
        )
    entity_assertions(expected, actual, test_results)
    assert_test(test_results)


def test_147():
    """
    Set a date reminder 30 days from now and remind me daily of the upcoming date.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time30 = DateTime(text="30 days from now")
    data_model.append(data_date_time30)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time1 = DateTime(text="daily", value="day 1")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="daily", value="day 2")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="daily", value="day 3")
    data_model.append(data_date_time3)

    # start code block to test
    date_time = DateTime.resolve_from_text("30 days from now")
    reminder = Reminders.create_reminder(date_time=date_time)

    person_reminded = Contact.resolve_from_text("me")
    date_times = DateTime.resolve_many_from_text("daily")
    content = Content.resolve_from_entity(entity=reminder)
    for date_time in date_times:
        Reminders.create_reminder(
            person_reminded=person_reminded, date_time=date_time, content=content
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": data_date_time30,
        }
    ] + [
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_time,
            "content": Content(value=reminder),
        }
        for data_date_time in [
            data_date_time1,
            data_date_time2,
            data_date_time3,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_148():
    """
    Is there a Radiohead concert in August, October, or November?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="a Radiohead concert")
    data_model.append(data_event_name)
    data_date_time1 = DateTime(text="August, October, or November", value="August")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="August, October, or November", value="October")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="August, October, or November", value="November")
    data_model.append(data_date_time3)
    data_date_time4 = DateTime(text="December", value="December")
    data_model.append(data_date_time4)
    data_event1 = EventEntity(event_name=data_event_name, date_time=data_date_time2)
    data_model.append(data_event1)
    data_event2 = EventEntity(event_name=data_event_name, date_time=data_date_time3)
    data_model.append(data_event2)
    data_event_neg = EventEntity(event_name=data_event_name, date_time=data_date_time4)
    data_model.append(data_event_neg)

    # start code block to test
    event_name = EventName.resolve_from_text("a Radiohead concert")
    date_times = DateTime.resolve_many_from_text("August, October, or November")
    events = []
    for date_time in date_times:
        events += Calendar.find_events(event_name=event_name, date_time=date_time)
    Responder.respond(response=events)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event1, data_event2]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_150_a():
    """
    Check the email to see that I received an email from Bob and reply to him.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type = MessageContentType(text="the email")
    data_model.append(data_message_content_type)
    data_sender = Contact(text="Bob")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Joe")
    data_model.append(data_sender_neg)
    data_message = MessageEntity(
        recipient=data_recipient,
        message_content_type=data_message_content_type,
        sender=data_sender,
    )
    data_model.append(data_message)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("the email")
    recipient = Contact.resolve_from_text("I")
    sender = Contact.resolve_from_text("Bob")
    messages = Messages.find_messages(
        message_content_type=message_content_type, recipient=recipient, sender=sender
    )
    test_messages = bool(messages)
    if test_messages:
        Messages.send_message(
            recipient=sender, message_content_type=message_content_type
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "message_content_type": data_message_content_type,
            "recipient": data_recipient,
            "sender": data_sender,
        },
        {
            "message_content_type": data_message_content_type,
            "recipient": data_sender,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_150_b():
    """
    Check the email to see that I received an email from Bob and reply to him.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type = MessageContentType(text="the email")
    data_model.append(data_message_content_type)
    data_sender = Contact(text="Bob")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Joe")
    data_model.append(data_sender_neg)
    data_message = MessageEntity(
        recipient=data_recipient,
        message_content_type=data_message_content_type,
        sender=data_sender_neg,
    )
    data_model.append(data_message)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("the email")
    recipient = Contact.resolve_from_text("I")
    sender = Contact.resolve_from_text("Bob")
    messages = Messages.find_messages(
        message_content_type=message_content_type, recipient=recipient, sender=sender
    )
    test_messages = bool(messages)
    if test_messages:
        Messages.send_message(
            recipient=sender, message_content_type=message_content_type
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "message_content_type": data_message_content_type,
            "recipient": data_recipient,
            "sender": data_sender_neg,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_154():
    """
    Check what the temperature is right now and set a reminder for me to grab my jacket.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="right now")
    data_model.append(data_date_time)
    data_temperature = WeatherTemperature(text="above 90")
    data_model.append(data_temperature)
    data_weather_forecast = WeatherForecastEntity(
        date_time=data_date_time, weather_temperature=data_temperature
    )
    data_model.append(data_weather_forecast)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="grab my jacket")
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("right now")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("grab my jacket")
    Reminders.create_reminder(person_reminded=person_reminded, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "content": data_content,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_155_a():
    """
    Check mail to check that Gemma messaged me and send a reply to her that I am doing ok.
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender = Contact(text="Gemma")
    data_model.append(data_sender)
    data_recipient = Contact(text="me")
    data_model.append(data_recipient)
    data_message = MessageEntity(sender=data_sender, recipient=data_recipient)
    data_model.append(data_message)
    data_content = Content(text="I am doing ok")
    data_model.append(data_content)

    # start code block to test
    sender = Contact.resolve_from_text("Gemma")
    recipient = Contact.resolve_from_text("me")
    messages = Messages.find_messages(recipient=recipient, sender=sender)
    test_messages = bool(messages)
    if test_messages:
        content = Content.resolve_from_text("I am doing ok")
        Messages.send_message(recipient=sender, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "sender": data_sender,
        },
        {
            "recipient": data_sender,
            "content": data_content,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_155_b():
    """
    Check mail to check that Gemma messaged me and send a reply to her that I am doing ok.
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender = Contact(text="Gemma")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Bono")
    data_model.append(data_sender_neg)
    data_recipient = Contact(text="me")
    data_model.append(data_recipient)
    data_message = MessageEntity(sender=data_sender_neg, recipient=data_recipient)
    data_model.append(data_message)
    data_content = Content(text="I am doing ok")
    data_model.append(data_content)

    # start code block to test
    sender = Contact.resolve_from_text("Gemma")
    recipient = Contact.resolve_from_text("me")
    messages = Messages.find_messages(recipient=recipient, sender=sender)
    test_messages = bool(messages)
    if test_messages:
        content = Content.resolve_from_text("I am doing ok")
        Messages.send_message(recipient=sender, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "sender": data_sender_neg,
            "recipient": data_recipient,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_162():
    """
    Play music at 3AM and play music again at 4AM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time3 = DateTime(text="at 3AM")
    data_model.append(data_date_time3)
    data_date_time4 = DateTime(text="at 4AM")
    data_model.append(data_date_time4)

    # start code block to test
    date_time = DateTime.resolve_from_text("at 3AM")
    Music.play_music(date_time=date_time)
    date_time = DateTime.resolve_from_text("at 4AM")
    Music.play_music(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MusicEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time3, data_date_time4]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_163():
    """
    Add Nutpods and coffee to my shopping list and email mom to ask her to stop by for coffee any day this week.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name1 = ProductName(text="Nutpods and coffee", value="Nutpods")
    data_model.append(data_product_name1)
    data_product_name2 = ProductName(text="Nutpods and coffee", value="coffee")
    data_model.append(data_product_name2)
    data_shopping_list_name = ShoppingListName(text="my shopping list")
    data_model.append(data_shopping_list_name)
    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="mom")
    data_model.append(data_recipient)
    data_content = Content(text="ask her to stop by for coffee any day this week")
    data_model.append(data_content)

    # start code block to test
    product_names = ProductName.resolve_many_from_text("Nutpods and coffee")
    shopping_list_name = ShoppingListName.resolve_from_text("my shopping list")
    for product_name in product_names:
        Shopping.add_to_shopping_list(
            shopping_list_name=shopping_list_name, product_name=product_name
        )

    message_content_type = MessageContentType.resolve_from_text("email")
    recipient = Contact.resolve_from_text("mom")
    content = Content.resolve_from_text(
        "ask her to stop by for coffee any day this week"
    )
    Messages.send_message(
        recipient=recipient, content=content, message_content_type=message_content_type
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ShoppingListEntity)
    expected = [
        {
            "shopping_list_name": data_shopping_list_name,
            "product_name": data_product_name,
        }
        for data_product_name in [data_product_name1, data_product_name2]
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "message_content_type": data_message_content_type,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_165():
    """
    Find the closest Walmart and get directions to there.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location1 = Location(
        text="the closest Walmart", value="Walmart midtown", closest=120
    )
    data_model.append(data_location1)
    data_location2 = Location(
        text="the closest Walmart", value="Walmart downtown", closest=35
    )
    data_model.append(data_location2)
    data_location3 = Location(
        text="the closest Walmart", value="Walmart uptown", closest=100
    )
    data_model.append(data_location3)
    data_navigation_direction1 = NavigationDirectionEntity(destination=data_location1)
    data_model.append(data_navigation_direction1)
    data_navigation_direction2 = NavigationDirectionEntity(destination=data_location2)
    data_model.append(data_navigation_direction2)
    data_navigation_direction3 = NavigationDirectionEntity(destination=data_location3)
    data_model.append(data_navigation_direction3)

    # start code block to test
    locations = Location.resolve_many_from_text("the closest Walmart")
    locations = utils.sort(locations, "closest")
    location = utils.first(locations)

    navigation_directions = Navigation.find_directions(destination=location)
    Responder.respond(response=navigation_directions)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction2]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_170():
    """
    See reminders and delete all reminders that are old.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="old")
    data_model.append(data_date_time)
    data_date_time_neg = DateTime(text="new")
    data_model.append(data_date_time_neg)
    reminder1 = ReminderEntity(date_time=data_date_time)
    data_model.append(reminder1)
    reminder2 = ReminderEntity(date_time=data_date_time_neg)
    data_model.append(reminder2)
    reminder3 = ReminderEntity(date_time=data_date_time)
    data_model.append(reminder3)

    # start code block to test
    date_time = DateTime.resolve_from_text("old")
    reminders = Reminders.find_reminders(date_time=date_time)
    Reminders.delete_reminders(reminders=reminders)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": data_date_time_neg,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_173_a():
    """
    Check there are messages from Jane and reply to her messages with "I am busy!"
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender = Contact(text="Jane")
    data_model.append(data_sender)
    data_message1 = MessageEntity(sender=data_sender)
    data_model.append(data_message1)
    data_message2 = MessageEntity(sender=data_sender)
    data_model.append(data_message2)
    data_content = Content(text="I am busy!")
    data_model.append(data_content)

    # start code block to test
    sender = Contact.resolve_from_text("Jane")
    messages = Messages.find_messages(sender=sender)
    test_messages = bool(messages)
    if test_messages:
        content = Content.resolve_from_text("I am busy!")
        Messages.send_message(recipient=sender, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "sender": data_sender,
        },
        {
            "sender": data_sender,
        },
        {
            "recipient": data_sender,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_173_b():
    """
    Check there are messages from Jane and reply to her messages with "I am busy!"
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender = Contact(text="Jane")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Carla")
    data_model.append(data_sender_neg)
    data_message1 = MessageEntity(sender=data_sender_neg)
    data_model.append(data_message1)
    data_message2 = MessageEntity(sender=data_sender_neg)
    data_model.append(data_message2)
    data_content = Content(text="I am busy!")
    data_model.append(data_content)

    # start code block to test
    sender = Contact.resolve_from_text("Jane")
    messages = Messages.find_messages(sender=sender)
    test_messages = bool(messages)
    if test_messages:
        content = Content.resolve_from_text("I am busy!")
        Messages.send_message(recipient=sender, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "sender": data_sender_neg,
        },
        {
            "sender": data_sender_neg,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_174_a():
    """
    Check that I received a mail from Jason or cancel my meeting later.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="a mail")
    data_model.append(data_message_content_type)
    data_sender = Contact(text="Jason")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Carla")
    data_model.append(data_sender_neg)
    data_message1 = MessageEntity(sender=data_sender)
    data_model.append(data_message1)
    data_message2 = MessageEntity(sender=data_sender_neg)
    data_model.append(data_message2)
    data_event_name = EventName(text="my meeting")
    data_model.append(data_event_name)
    data_date_time = DateTime(text="later")
    data_model.append(data_date_time)
    data_date_time_neg = DateTime(text="now")
    data_model.append(data_date_time_neg)
    data_event = EventEntity(event_name=data_event_name, date_time=data_date_time)
    data_model.append(data_event)
    data_event = EventEntity(event_name=data_event_name, date_time=data_date_time_neg)
    data_model.append(data_event)

    # start code block to test
    sender = Contact.resolve_from_text("Jason")
    messages = Messages.find_messages(sender=sender)
    test_messages = bool(messages)
    if not test_messages:
        event_name = EventName.resolve_from_text("my meeting")
        date_time = DateTime.resolve_from_text("later")
        Calendar.delete_events(event_name=event_name, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventEntity)
    expected = [
        {"event_name": data_event_name, "date_time": data_date_time},
        {"event_name": data_event_name, "date_time": data_date_time_neg},
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_174_b():
    """
    Check that I received a mail from Jason or cancel my meeting later.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="a mail")
    data_model.append(data_message_content_type)
    data_sender = Contact(text="Jason")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Carla")
    data_model.append(data_sender_neg)
    data_message1 = MessageEntity(sender=data_sender_neg)
    data_model.append(data_message1)
    data_message2 = MessageEntity(sender=data_sender_neg)
    data_model.append(data_message2)
    data_event_name = EventName(text="my meeting")
    data_model.append(data_event_name)
    data_date_time = DateTime(text="later")
    data_model.append(data_date_time)
    data_date_time_neg = DateTime(text="now")
    data_model.append(data_date_time_neg)
    data_event = EventEntity(event_name=data_event_name, date_time=data_date_time)
    data_model.append(data_event)
    data_event = EventEntity(event_name=data_event_name, date_time=data_date_time_neg)
    data_model.append(data_event)

    # start code block to test
    sender = Contact.resolve_from_text("Jason")
    messages = Messages.find_messages(sender=sender)
    test_messages = bool(messages)
    if not test_messages:
        event_name = EventName.resolve_from_text("my meeting")
        date_time = DateTime.resolve_from_text("later")
        Calendar.delete_events(event_name=event_name, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventEntity)
    expected = [
        {"event_name": data_event_name, "date_time": data_date_time_neg},
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_175():
    """
    Set navigation for walking to the park, show me how long it took me to get there.
    """
    # test data
    data_model = DataModel(reset=True)
    data_nav_travel_method = NavigationTravelMethod(text="by walking")
    data_model.append(data_nav_travel_method)
    data_destination = Location(text="to the park")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(
        nav_travel_method=data_nav_travel_method, destination=data_destination
    )
    data_model.append(data_navigation_direction)
    data_navigation_duration = NavigationDurationEntity(
        nav_travel_method=data_nav_travel_method, destination=data_destination
    )
    data_model.append(data_navigation_duration)

    # start code block to test
    nav_travel_method = NavigationTravelMethod.resolve_from_text("by walking")
    destination = Location.resolve_from_text("to the park")
    navigation_directions = Navigation.find_directions(
        destination=destination, nav_travel_method=nav_travel_method
    )
    Responder.respond(response=navigation_directions)

    navigation_durations = Navigation.find_duration(
        destination=destination, nav_travel_method=nav_travel_method
    )
    Responder.respond(response=navigation_durations)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationDurationEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_duration]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_181():
    """
    Message Jessica to see what time she can go to the movies Saturday and get tickets for any horror movie playing at that time.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="Jessica")
    data_model.append(data_recipient)
    data_content = Content(text="see what time she can go to the movies Saturday")
    data_model.append(data_content)
    data_event_name1 = EventName(
        text="any horror movie playing", value="Nightmare on Elm Street"
    )
    data_model.append(data_event_name1)
    data_event_name2 = EventName(text="any horror movie playing", value="Hostel")
    data_model.append(data_event_name2)
    data_date_time = DateTime(text="at that time")
    data_model.append(data_date_time)

    # start code block to test
    recipient = Contact.resolve_from_text("Jessica")
    content = Content.resolve_from_text(
        "see what time she can go to the movies Saturday"
    )
    Messages.send_message(recipient=recipient, content=content)

    event_name = EventName.resolve_from_text("any horror movie")
    date_time = DateTime.resolve_from_text("at that time")
    Calendar.purchase_tickets(event_name=event_name, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {"recipient": data_recipient, "content": data_content},
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(EventTicketEntity)
    expected = [
        {"event_name": data_event_name1, "date_time": data_date_time},
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_184():
    """
    Is it going to be cold on Tue, Wed at 5 PM?
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="cold")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="hot")
    data_model.append(data_weather_attribute_neg)
    data_date_time1 = DateTime(text="on Tue, Wed at 5 PM", value="Tuesday")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="on Tue, Wed at 5 PM", value="Wednesday")
    data_model.append(data_date_time2)
    data_weather_forecast1 = WeatherForecastEntity(
        weather_attribute=data_weather_attribute, date_time=data_date_time1
    )
    data_model.append(data_weather_forecast1)
    data_weather_forecast2 = WeatherForecastEntity(
        weather_attribute=data_weather_attribute_neg, date_time=data_date_time2
    )
    data_model.append(data_weather_forecast2)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("cold")
    date_times = DateTime.resolve_many_from_text("on Tue, Wed at 5 PM")
    weather_forecasts = []
    for date_time in date_times:
        weather_forecasts += Weather.find_weather_forecasts(
            weather_attribute=weather_attribute, date_time=date_time
        )
    Responder.respond(response=weather_forecasts)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast1]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_185():
    """
    Search for pillows on Amazon under $40, show me the highest rated one.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name = ProductName(text="pillows")
    data_model.append(data_product_name)
    data_location = Location(text="on Amazon")
    data_model.append(data_location)
    data_location_neg = Location(text="Target")
    data_model.append(data_location_neg)
    data_product_attribute = ProductAttribute(text="under $40")
    data_model.append(data_product_attribute)
    data_product1 = ProductEntity(
        product_name=data_product_name,
        location=data_location,
        product_attribute=data_product_attribute,
        rated=1,
    )
    data_model.append(data_product1)
    data_product2 = ProductEntity(
        product_name=data_product_name,
        location=data_location,
        product_attribute=data_product_attribute,
        rated=10,
    )
    data_model.append(data_product2)
    data_product3 = ProductEntity(
        product_name=data_product_name,
        location=data_location_neg,
        product_attribute=data_product_attribute,
        rated=100,
    )
    data_model.append(data_product3)

    # start code block to test
    product_name = ProductName.resolve_from_text("pillows")
    location = Location.resolve_from_text("on Amazon")
    product_attribute = ProductAttribute.resolve_from_text("under $40")
    products = Shopping.find_products(
        product_name=product_name,
        location=location,
        product_attribute=product_attribute,
    )
    products = utils.sort(products, "rated")
    product = utils.first(products)
    Responder.respond(response=product)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response(ProductEntity))
    actual = next(iterator, None)
    expected = data_product1
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_188():
    """
    Remind me of the ball game later on, set a reminder every 30 minutes before the game.
    """
    # test data
    data_model = DataModel(reset=True)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="of the ball game later on")
    data_model.append(data_content)
    data_date_time1 = DateTime(text="every 30 minutes before the game", value="16:30")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="every 30 minutes before the game", value="17:00")
    data_model.append(data_date_time2)

    # start code block to test
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("of the ball game later on")
    date_times = DateTime.resolve_many_from_text("every 30 minutes before the game")
    for date_time in date_times:
        Reminders.create_reminder(
            person_reminded=person_reminded, content=content, date_time=date_time
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "content": data_content,
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time1, data_date_time2]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_189():
    """
    Set a reminder every weekday at 5PM to take the bus home.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(text="every weekday at 5PM", value="17:00 Mon")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="every weekday at 5PM", value="17:00 Tue")
    data_model.append(data_date_time2)
    data_content = Content(text="take the bus home")
    data_model.append(data_content)

    # start code block to test
    date_times = DateTime.resolve_many_from_text("every weekday at 5PM")
    content = Content.resolve_from_text("take the bus home")
    for date_time in date_times:
        Reminders.create_reminder(content=content, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "content": data_content,
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time1, data_date_time2]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_190():
    """
    Set an alarm the day before each of my appointments in May, June, July.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name1 = EventName(text="each of my appointments", value="A")
    data_model.append(data_event_name1)
    data_event_name2 = EventName(text="each of my appointments", value="B")
    data_model.append(data_event_name2)
    data_date_time1 = DateTime(text="in May, June, July", value="May")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="in May, June, July", value="June")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="in May, June, July", value="July")
    data_model.append(data_date_time3)
    data_event1 = EventEntity(event_name=data_event_name1, date_time=data_date_time2)
    data_model.append(data_event1)
    data_event2 = EventEntity(event_name=data_event_name2, date_time=data_date_time1)
    data_model.append(data_event2)
    data_date_time_event1 = DateTime(value=data_event1)
    data_model.append(data_date_time_event1)
    data_date_time_event2 = DateTime(value=data_event2)
    data_model.append(data_date_time_event2)

    # start code block to test
    event_names = EventName.resolve_many_from_text("each of my appointments")
    date_times = DateTime.resolve_many_from_text("in May, June, July")
    events = []
    for event_name in event_names:
        for date_time in date_times:
            events += Calendar.find_events(event_name=event_name, date_time=date_time)

    for event in events:
        date_time = DateTime.resolve_from_entity(event)
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time_event1, data_date_time_event2]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_191():
    """
    Set timer to wake me up in 3 hours at 5, 6, 7 AM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(text="in 3 hours at 5, 6, 7 AM", value="5:00")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="in 3 hours at 5, 6, 7 AM", value="6:00")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="in 3 hours at 5, 6, 7 AM", value="7:00")
    data_model.append(data_date_time3)

    # start code block to test
    date_times = DateTime.resolve_many_from_text("in 3 hours at 5, 6, 7 AM")
    for date_time in date_times:
        Timer.create_timer(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(TimerEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time1, data_date_time2, data_date_time3]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_192():
    """
    Set an alarm to remind me of my meeting at 4 PM between 5PM every 10 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(
        text="at 4 PM between 5PM every 10 minutes", value="16:00"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="at 4 PM between 5PM every 10 minutes", value="16:10"
    )
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(
        text="at 4 PM between 5PM every 10 minutes", value="16:20"
    )
    data_model.append(data_date_time3)
    data_date_time4 = DateTime(
        text="at 4 PM between 5PM every 10 minutes", value="16:30"
    )
    data_model.append(data_date_time4)

    # start code block to test
    date_times = DateTime.resolve_many_from_text("at 4 PM between 5PM every 10 minutes")
    for date_time in date_times:
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
        for data_date_time in [
            data_date_time1,
            data_date_time2,
            data_date_time3,
            data_date_time4,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_193():
    """
    Set navigation to the the airport, text Susie I will meet her there at 8 a.m.
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination = Location(text="the airport")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)
    data_recipient = Contact(text="Susie")
    data_model.append(data_recipient)
    data_content = Content(text="I will meet her there at 8 a.m")
    data_model.append(data_content)

    # start code block to test
    destination = Location.resolve_from_text("the airport")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)

    recipient = Contact.resolve_from_text("Susie")
    content = Content.resolve_from_text("I will meet her there at 8 a.m")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_194():
    """
    Blast music at 5AM, 6AM, 7AM until I wake up
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(text="at 5AM, 6AM, 7AM", value="5Am")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="at 5AM, 6AM, 7AM", value="6Am")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="at 5AM, 6AM, 7AM", value="7Am")
    data_model.append(data_date_time3)

    # start code block to test
    date_times = DateTime.resolve_many_from_text("at 5AM, 6AM, 7AM")
    for date_time in date_times:
        Music.play_music(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MusicEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time1, data_date_time2, data_date_time3]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_195():
    """
    Check that it's hot on Tues, Weds, Thu and set a reminder for the zoo on any day it's hot.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="hot")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="cold")
    data_model.append(data_weather_attribute_neg)
    data_date_time1 = DateTime(text="on Tues, Weds, Thu", value="Tuesday")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="on Tues, Weds, Thu", value="Wedneday")
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(text="on Tues, Weds, Thu", value="Thursday")
    data_model.append(data_date_time3)
    data_weather_forecast1 = WeatherForecastEntity(
        date_time=data_date_time1, weather_attribute=data_weather_attribute_neg
    )
    data_model.append(data_weather_forecast1)
    data_weather_forecast2 = WeatherForecastEntity(
        date_time=data_date_time2, weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast2)
    data_weather_forecast3 = WeatherForecastEntity(
        date_time=data_date_time3, weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast3)
    data_date_time1 = DateTime(value=data_weather_forecast1)
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(value=data_weather_forecast2)
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(value=data_weather_forecast3)
    data_model.append(data_date_time3)
    data_content = Content(text="the zoo")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("hot")
    date_times = DateTime.resolve_many_from_text("on Tues, Weds, Thu")
    weather_forecasts = []
    for date_time in date_times:
        weather_forecasts += Weather.find_weather_forecasts(
            weather_attribute=weather_attribute, date_time=date_time
        )
    Responder.respond(response=weather_forecasts)

    content = Content.resolve_from_text("the zoo")
    for weather_forecast in weather_forecasts:
        date_time = DateTime.resolve_from_entity(entity=weather_forecast)
        Reminders.create_reminder(content=content, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast2, data_weather_forecast3]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "content": data_content,
            "date_time": data_date_time,
        }
        for data_date_time in [data_date_time2, data_date_time3]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_199():
    """
    Order 1 green beans, 2 chickens, and broth from the store.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name1 = ProductName(
        text="1 green beans, 2 chickens, and broth", value="1 green beans"
    )
    data_model.append(data_product_name1)
    data_product_name2 = ProductName(
        text="1 green beans, 2 chickens, and broth", value="2 chickens"
    )
    data_model.append(data_product_name2)
    data_product_name3 = ProductName(
        text="1 green beans, 2 chickens, and broth", value="broth"
    )
    data_model.append(data_product_name3)
    data_location = Location(text="the store")
    data_model.append(data_location)

    # start code block to test
    product_names = ProductName.resolve_many_from_text(
        "1 green beans, 2 chickens, and broth"
    )
    location = Location.resolve_from_text("the store")
    for product_name in product_names:
        Shopping.order(product_name=product_name, location=location)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(OrderEntity)
    expected = [
        {
            "product_name": data_product_name,
            "location": data_location,
        }
        for data_product_name in [
            data_product_name1,
            data_product_name2,
            data_product_name3,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_205():
    """
    Set alarm in 30 minutes and repeat alarm every 40 minutes for the next 2 hours.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time0 = DateTime(text="in 30 minutes")
    data_model.append(data_date_time0)
    data_date_time1 = DateTime(
        text="every 40 minutes for the next 2 hours", value="02:40"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="every 40 minutes for the next 2 hours", value="03:20"
    )
    data_model.append(data_date_time2)
    data_date_time3 = DateTime(
        text="every 40 minutes for the next 2 hours", value="03:40"
    )
    data_model.append(data_date_time3)

    # start code block to test
    date_time = DateTime.resolve_from_text("in 30 minutes")
    Alarm.create_alarm(date_time=date_time)

    date_times = DateTime.resolve_many_from_text(
        "every 40 minutes for the next 2 hours"
    )
    for date_time in date_times:
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
        for data_date_time in [
            data_date_time0,
            data_date_time1,
            data_date_time2,
            data_date_time3,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_207():
    """
    Remind me on the 10th to reserve airline tickets and message Ashleigh with the confirmation.
    """
    # test data
    data_model = DataModel(reset=True)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time = DateTime(text="the 10th")
    data_model.append(data_date_time)
    data_content = Content(
        text="reserve airline tickets and message Ashleigh with the confirmation"
    )
    data_model.append(data_content)

    # start code block to test
    person_reminded = Contact.resolve_from_text("me")
    date_time = DateTime.resolve_from_text("the 10th")
    content = Content.resolve_from_text(
        "reserve airline tickets and message Ashleigh with the confirmation"
    )
    Reminders.create_reminder(
        person_reminded=person_reminded, date_time=date_time, content=content
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_time,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_208():
    """
    Will there be any free events downtown this weekend or next weekend?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="free events")
    data_model.append(data_event_name)
    data_location = Location(text="downtown")
    data_model.append(data_location)
    data_date_time1 = DateTime(
        text="this weekend or next weekend", value="this weekend"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="this weekend or next weekend", value="next weekend"
    )
    data_model.append(data_date_time2)
    data_event = EventEntity(
        event_name=data_event_name, location=data_location, date_time=data_date_time2
    )
    data_model.append(data_event)

    # start code block to test
    event_name = EventName.resolve_from_text("free events")
    location = Location.resolve_from_text("downtown")
    date_times = DateTime.resolve_many_from_text("this weekend or next weekend")
    events = []
    for date_time in date_times:
        events += Calendar.find_events(
            event_name=event_name, location=location, date_time=date_time
        )
    Responder.respond(response=events)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_209_a():
    """
    Set the alarm at 6 a.m. should it be a rainy day.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="at 6 a.m.")
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="a rainy day")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute_neg)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("a rainy day")
    weather_forecasts = WeatherForecastEntity(weather_attribute=weather_attribute)
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        date_time = DateTime.resolve_from_text("at 6 a.m.")
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_209_b():
    """
    Set the alarm at 6 a.m. should it be a rainy day.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="at 6 a.m.")
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="a rainy day")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute_neg)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute_neg
    )
    data_model.append(data_weather_forecast)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("a rainy day")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        date_time = DateTime.resolve_from_text("at 6 a.m.")
        Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_211():
    """
    Check my calendar to see what time the board meeting is on Wednesday and set an alarm when the meeting is supposed to start.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)
    data_event_name = EventName(text="the board meeting")
    data_model.append(data_event_name)
    data_date_time = DateTime(text="on Wednesday")
    data_model.append(data_date_time)
    data_event = EventEntity(
        event_calendar=data_event_calendar,
        event_name=data_event_name,
        date_time=data_date_time,
    )
    data_model.append(data_event)
    data_date_time_alarm = DateTime(
        # text="30 minutes before the meeting is supposed to start",
        value=[data_event]
    )
    data_model.append(data_date_time_alarm)

    # start code block to test
    event_calendar = EventCalendar.resolve_from_text("my calendar")
    event_name = EventName.resolve_from_text("the board meeting")
    date_time = DateTime.resolve_from_text("on Wednesday")
    events = Calendar.find_events(
        event_calendar=event_calendar, event_name=event_name, date_time=date_time
    )

    date_time = DateTime.resolve_from_entity(
        entity=events,  # text="30 minutes before the meeting is supposed to start"
    )
    Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {
            "date_time": data_date_time_alarm,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_213():
    """
    Move any text messages that mention dinner and are between two weeks and one month old to the trash folder.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="text messages")
    data_model.append(data_message_content_type)
    data_content = Content(text="mention dinner")
    data_model.append(data_content)
    data_content_neg = Content(text="breakfast")
    data_model.append(data_content_neg)
    data_date_time1 = DateTime(
        text="between two weeks and one month old", value="3 weeks"
    )
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(
        text="between two weeks and one month old", value="4 weeks"
    )
    data_model.append(data_date_time2)
    data_message1 = MessageEntity(
        message_content_type=data_message_content_type,
        content=data_content,
        date_time=data_date_time1,
    )
    data_model.append(data_message1)
    data_message2 = MessageEntity(
        message_content_type=data_message_content_type,
        content=data_content,
        date_time=data_date_time2,
    )
    data_model.append(data_message2)
    data_message3 = MessageEntity(
        message_content_type=data_message_content_type,
        content=data_content_neg,
        date_time=data_date_time2,
    )
    data_model.append(data_message3)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("text messages")
    content = Content.resolve_from_text("mention dinner")
    date_times = DateTime.resolve_many_from_text("between two weeks and one month old")
    messages = []
    for date_time in date_times:
        messages += Messages.find_messages(
            message_content_type=message_content_type,
            content=content,
            date_time=date_time,
        )
    Messages.delete_messages(messages=messages)

    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "message_content_type": data_message_content_type,
            "content": data_content_neg,
            "date_time": data_date_time2,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_214():
    """
    Purchase tickets for the NFL game Friday and text all my friends that I am going to be busy that day.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="the NFL game")
    data_model.append(data_event_name)
    data_date_time = DateTime(text="Friday")
    data_model.append(data_date_time)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_contact1 = Contact(text="all my friends", value="John")
    data_model.append(data_contact1)
    data_contact2 = Contact(text="all my friends", value="Abigail")
    data_model.append(data_contact2)
    data_content = Content(text="I am going to be busy that day")
    data_model.append(data_content)

    # start code block to test
    event_name = EventName.resolve_from_text("the NFL game")
    date_time = DateTime.resolve_from_text("Friday")
    Calendar.purchase_tickets(event_name=event_name, date_time=date_time)

    message_content_type = MessageContentType.resolve_from_text("text")
    recipients = Contact.resolve_many_from_text("all my friends")
    content = Content.resolve_from_text("I am going to be busy that day")
    for recipient in recipients:
        Messages.send_message(
            message_content_type=message_content_type,
            recipient=recipient,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventTicketEntity)
    expected = [
        {
            "event_name": data_event_name,
            "date_time": data_date_time,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
        }
        for data_recipient in [
            data_contact1,
            data_contact2,
        ]
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_216_a():
    """
    Check my email to see whether Soeurette has RSVPed for this evening's party; assuming she's planning to come, send her the directions to the venue.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="my email")
    data_model.append(data_message_content_type)
    data_sender = Contact(text="Soeurette")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Sam")
    data_model.append(data_sender_neg)
    data_content = Content(text="has RSVPed for this evening's party")
    data_model.append(data_content)
    data_content_neg = Content(text="decline")
    data_model.append(data_content_neg)
    data_message1 = MessageEntity(
        message_content_type=data_message_content_type,
        sender=data_sender,
        content=data_content,
    )
    data_model.append(data_message1)
    data_message2 = MessageEntity(
        message_content_type=data_message_content_type,
        sender=data_sender_neg,
        content=data_content_neg,
    )
    data_model.append(data_message2)
    data_destination = Location(text="the venue")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)
    data_content_directions = Content(value=[data_navigation_direction])
    data_model.append(data_content_directions)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("my email")
    sender = Contact.resolve_from_text("Soeurette")
    content = Content.resolve_from_text("has RSVPed for this evening's party")
    messages = Messages.find_messages(
        message_content_type=message_content_type, sender=sender, content=content
    )
    test_messages = bool(messages)
    if test_messages:
        destination = Location.resolve_from_text("the venue")
        navigation_directions = Navigation.find_directions(destination=destination)
        content = Content.resolve_from_entity(navigation_directions)
        Messages.send_message(recipient=sender, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "message_content_type": data_message_content_type,
            "sender": data_sender,
            "content": data_content,
        },
        {
            "message_content_type": data_message_content_type,
            "sender": data_sender_neg,
            "content": data_content_neg,
        },
        {
            "recipient": data_sender,
            "content": data_content_directions,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_216_b():
    """
    Check my email to see whether Soeurette has RSVPed for this evening's party; assuming she's planning to come, send her the directions to the venue.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="my email")
    data_model.append(data_message_content_type)
    data_sender = Contact(text="Soeurette")
    data_model.append(data_sender)
    data_sender_neg = Contact(text="Sam")
    data_model.append(data_sender_neg)
    data_content = Content(text="has RSVPed for this evening's party")
    data_model.append(data_content)
    data_content_neg = Content(text="decline")
    data_model.append(data_content_neg)
    data_message1 = MessageEntity(
        message_content_type=data_message_content_type,
        sender=data_sender,
        content=data_content_neg,
    )
    data_model.append(data_message1)
    data_message2 = MessageEntity(
        message_content_type=data_message_content_type,
        sender=data_sender_neg,
        content=data_content_neg,
    )
    data_model.append(data_message2)
    data_destination = Location(text="the venue")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)
    data_content_directions = Content(value=[data_navigation_direction])
    data_model.append(data_content_directions)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("my email")
    sender = Contact.resolve_from_text("Soeurette")
    content = Content.resolve_from_text("has RSVPed for this evening's party")
    messages = Messages.find_messages(
        message_content_type=message_content_type, sender=sender, content=content
    )
    test_messages = bool(messages)
    if test_messages:
        destination = Location.resolve_from_text("the venue")
        navigation_directions = Navigation.find_directions(destination=destination)
        content = Content.resolve_from_entity(navigation_directions)
        Messages.send_message(recipient=sender, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "message_content_type": data_message_content_type,
            "sender": data_sender,
            "content": data_content_neg,
        },
        {
            "message_content_type": data_message_content_type,
            "sender": data_sender_neg,
            "content": data_content_neg,
        },
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_218():
    """
    Set an alarm for 6 AM and set a reminder to go shopping at 4 PM Wednesday.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="for 6 AM")
    data_model.append(data_date_time)
    data_content = Content(text="go shopping")
    data_model.append(data_content)
    data_date_time_reminder = DateTime(text="at 4 PM Wednesday")
    data_model.append(data_date_time_reminder)

    # start code block to test
    date_time = DateTime.resolve_from_text("for 6 AM")
    Alarm.create_alarm(date_time=date_time)

    content = Content.resolve_from_text("go shopping")
    date_time = DateTime.resolve_from_text("at 4 PM Wednesday")
    Reminders.create_reminder(content=content, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [
        {
            "date_time": data_date_time,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": data_date_time_reminder,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_238():
    """
    On evenings the temperature drops below 50F, turn the family room heat to 70F.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(text="evenings", value="Monday evening")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="evenings", value="Tuesday evening")
    data_model.append(data_date_time2)
    data_weather_temperature = WeatherTemperature(text="below 50F")
    data_model.append(data_weather_temperature)
    data_weather_temperature_neg = WeatherTemperature(text="48F")
    data_model.append(data_weather_temperature_neg)
    data_weather_forecast1 = WeatherForecastEntity(
        date_time=data_date_time1, weather_temperature=data_weather_temperature
    )
    data_model.append(data_weather_forecast1)
    data_weather_forecast2 = WeatherForecastEntity(
        date_time=data_date_time2, weather_temperature=data_weather_temperature_neg
    )
    data_model.append(data_weather_forecast2)
    data_date_time_weather1 = DateTime(value=data_weather_forecast1)
    data_model.append(data_date_time_weather1)
    data_date_time_weather2 = DateTime(value=data_weather_forecast2)
    data_model.append(data_date_time_weather2)
    data_home_device_action = HomeDeviceAction(text="turn")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the family room heat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="to 70F")
    data_model.append(data_home_device_value)

    # start code block to test
    date_times = DateTime.resolve_many_from_text("On evenings")
    weather_temperature = WeatherTemperature.resolve_from_text("below 50F")
    weather_forecasts = []
    for date_time in date_times:
        weather_forecasts += Weather.find_weather_forecasts(
            date_time=date_time, weather_temperature=weather_temperature
        )

    for weather_forecast in weather_forecasts:
        date_time = DateTime.resolve_from_entity(entity=weather_forecast)
        home_device_action = HomeDeviceAction.resolve_from_text("turn")
        home_device_name = HomeDeviceName.resolve_from_text("the family room heat")
        home_device_value = HomeDeviceValue.resolve_from_text("to 70F")
        SmartHome.execute_home_device_action(
            date_time=date_time,
            device_action=home_device_action,
            device_name=home_device_name,
            device_value=home_device_value,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "date_time": data_date_time_weather1,
            "device_action": data_home_device_action,
            "device_name": data_home_device_name,
            "device_value": data_home_device_value,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)
