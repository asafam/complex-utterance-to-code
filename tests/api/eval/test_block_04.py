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
from utils.test_utils import *


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
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
    expected = [data_place]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
    expected = [data_event1, data_event2, data_event3]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
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
    actual = next(iterator)
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
    data_event_name = Content(text="the art festival")
    data_model.append(data_event_name)
    data_date_time1 = DateTime(text="this weekend", value="Saturday")
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="this weekend", value="Sunday")
    data_model.append(data_date_time2)
    data_event1 = EventEntity(name=data_event_name, date_time=data_date_time1)
    data_model.append(data_event1)
    data_event2 = EventEntity(name=data_event_name, date_time=data_date_time2)
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

    events = Calendar.find_event(event_name=event_name)
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
    actual = next(iterator)
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
    data_recipient = Contact(text="manager Steve")
    data_model.append(data_recipient)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_content = Content(text="a text confirmation for the meeting from Jennie")
    data_model.append(data_content)
    data_message = MessageEntity(content=data_content, recipient=data_recipient)
    data_model.append(data_message)

    # start code block to test
    recipient = Contact.resolve_from_text("I")
    content = Content.resolve_from_text(
        "a text confirmation for the meeting from Jennie"
    )
    messages = Messages.find_messages(recipient=recipient, content=content)
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
        {"recipient": data_recipient, "message_content_type": data_message_content_type}
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
    data_recipient = Contact(text="manager Steve")
    data_model.append(data_recipient)
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_content = Content(text="a text confirmation for the meeting from Jennie")
    data_model.append(data_content)

    # start code block to test
    recipient = Contact.resolve_from_text("I")
    content = Content.resolve_from_text(
        "a text confirmation for the meeting from Jennie"
    )
    messages = Messages.find_messages(recipient=recipient, content=content)
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
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)
