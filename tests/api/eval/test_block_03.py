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


def test_52():
    """
    Set a reminder at 3:00 PM that I will need to pick up my items from the store, and text Jason to meet me at the store at 2:50 PM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="at 3 PM")
    data_model.append(data_date_time)
    data_content = Content(
        text="I will need to pick up my items from the store",
    )
    data_model.append(data_content)
    data_message_content_type = MessageContentType(text="text")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Jason")
    data_model.append(data_recipient)
    data_content_message = Content(text="meet me at the store at 2:50 PM")
    data_model.append(data_content_message)

    # start code block to test
    date_time = DateTime.resolve_from_text("at 3 PM")
    content = Content.resolve_from_text(
        "I will need to pick up my items from the store"
    )
    Reminders.create_reminder(date_time=date_time, content=content)

    message_content_type = MessageContentType.resolve_from_text("text")
    recipient = Contact.resolve_from_text("Jason")
    content = Content.resolve_from_text("meet me at the store at 2:50 PM")
    Messages.send_message(
        recipient=recipient, content=content, message_content_type=message_content_type
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [{"date_time": data_date_time, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content_message,
            "message_content_type": data_message_content_type,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_54():
    """
    Set the thermostat to 70 degrees and play my romantic playlist.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_action = HomeDeviceAction(text="set")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="70 degrees")
    data_model.append(data_home_device_value)
    data_playlist = Playlist(text="my romantic playlist", value="my romantic playlist")
    data_model.append(data_playlist)

    # start code block to test
    device_action = HomeDeviceAction.resolve_from_text("set")
    device_name = HomeDeviceName.resolve_from_text("the thermostat")
    device_value = HomeDeviceValue.resolve_from_text("70 degrees")
    SmartHome.execute_home_device_action(
        device_action=device_action, device_name=device_name, device_value=device_value
    )

    playlist = Playlist.resolve_from_text("my romantic playlist")
    Music.play_music(playlist=playlist)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_name": data_home_device_name,
            "device_action": data_home_device_action,
            "device_value": data_home_device_value,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MusicEntity)
    expected = [{"playlist": data_playlist}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_55():
    """
    Remind me to send an email to Mom and Dad tomorrow and delete the appointment in my calendar for Tuesday.
    """
    # test data
    data_model = DataModel(reset=True)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="send an email to Mom and Dad")
    data_model.append(data_content)
    data_date_time = DateTime(text="Tuesday")
    data_model.append(data_date_time)
    data_date_time2 = DateTime(text="Wednesday")
    data_model.append(data_date_time2)
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_event1 = EventEntity(date_time=data_date_time, event_calendar=data_calendar)
    data_model.append(data_event1)
    data_event2 = EventEntity(date_time=data_date_time2, event_calendar=data_calendar)
    data_model.append(data_event2)

    # start code block to test
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("send an email to Mom and Dad")
    Reminders.create_reminder(person_reminded=person_reminded, content=content)

    event_calendar = EventCalendar.resolve_from_text("my calendar")
    date_time = DateTime.resolve_from_text("Tuesday")
    Calendar.delete_events(event_calendar=event_calendar, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [{"person_reminded": data_person_reminded, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(EventEntity)
    expected = [{"date_time": data_date_time2, "event_calendar": data_calendar}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_58_a():
    """
    If Walmart has Jurassic World on bluray, buy it so I can pick it up tomorrow morning.
    """
    # test data
    data_model = DataModel(reset=True)
    data_store = Location(text="Walmart")
    data_model.append(data_store)
    data_product_name = ProductName(text="Jurassic World on bluray")
    data_model.append(data_product_name)
    data_product = ProductEntity(location=data_store, product_name=data_product_name)
    data_model.append(data_product)

    # start code block to test
    location = Location.resolve_from_text("Walmart")
    product_name = ProductName.resolve_from_text("Jurassic World on bluray")
    products = Shopping.find_products(location=location, product_name=product_name)
    test_products = bool(products)
    if test_products:
        Shopping.order(product_name=product_name, location=location)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(OrderEntity)
    expected = [{"product_name": data_product_name, "location": data_store}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_58_b():
    """
    If Walmart has Jurassic World on bluray, buy it so I can pick it up tomorrow morning.
    """
    # test data
    data_model = DataModel(reset=True)
    data_store1 = Location(text="Amazon")
    data_model.append(data_store1)
    data_store2 = Location(text="Walmart")
    data_model.append(data_store2)
    data_product_name = ProductName(text="Jurassic World on bluray")
    data_model.append(data_product_name)
    data_product = ProductEntity(location=data_store1, product_name=data_product_name)
    data_model.append(data_product)

    # start code block to test
    location = Location.resolve_from_text("Walmart")
    product_name = ProductName.resolve_from_text("Jurassic World on bluray")
    products = Shopping.find_products(location=location, product_name=product_name)
    test_products = bool(products)
    if test_products:
        Shopping.order(product_name=product_name, location=location)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(OrderEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_59():
    """
    Get directions to Portland, and tell me if it will snow along the route in the next hour
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination = Location(text="Portland")
    data_model.append(data_destination)
    data_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_direction)
    data_weather_attribute = WeatherAttribute(text="snow")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(
        text="in the next hour",
    )
    data_model.append(data_date_time)
    data_location = Location(value=data_direction)
    data_model.append(data_location)
    data_weather_forecast = WeatherForecastEntity(
        location=data_location,
        weather_attribute=data_weather_attribute,
        date_time=data_date_time,
    )
    data_model.append(data_weather_forecast)

    # start code block to test
    destination = Location.resolve_from_text("Portland")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)

    weather_attribute = WeatherAttribute.resolve_from_text("snow")
    date_time = DateTime.resolve_from_text("in the next hour")
    weather_forecasts = []
    for navigation_direction in navigation_directions:
        location = Location.resolve_from_entity(navigation_direction)
        weather_forecasts += Weather.find_weather_forecasts(
            weather_attribute=weather_attribute, location=location, date_time=date_time
        )
    Responder.respond(response=weather_forecasts)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator)
    expected = [data_direction]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_60_a():
    """
    Check the weather and text Mike that I will meet them later if it's hot.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="hot")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="cold")
    data_model.append(data_weather_attribute2)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute1
    )
    data_model.append(data_weather_forecast)
    data_recipient = Contact(text="Mike")
    data_model.append(data_recipient)
    data_content = Content(text="I will meet them later")
    data_model.append(data_content)

    # start code block to test
    weather_forecasts = Weather.find_weather_forecasts()
    Responder.respond(response=weather_forecasts)

    weather_attribute = WeatherAttribute.resolve_from_text("hot")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_attribute=weather_attribute
    )
    test_weather = bool(weather_forecasts)
    if test_weather:
        recipient = Contact.resolve_from_text("Mike")
        content = Content.resolve_from_text("I will meet them later")
        Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_60_b():
    """
    Check the weather and text Mike that I will meet them later if it's hot.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="hot")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="cold")
    data_model.append(data_weather_attribute2)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute2
    )
    data_model.append(data_weather_forecast)
    data_recipient = Contact(text="Mike")
    data_model.append(data_recipient)
    data_content = Content(text="I will meet them later")
    data_model.append(data_content)

    # start code block to test
    weather_forecasts = Weather.find_weather_forecasts()
    Responder.respond(response=weather_forecasts)

    weather_attribute = WeatherAttribute.resolve_from_text("hot")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_attribute=weather_attribute
    )
    test_weather = bool(weather_forecasts)
    if test_weather:
        recipient = Contact.resolve_from_text("Mike")
        content = Content.resolve_from_text("I will meet them later")
        Messages.send_message(recipient=recipient, content=content)
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


def test_63_a():
    """
    If the weather is going to be sunny Saturday morning, send an email to Ashley asking if she wants to go for a hike.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="cloudy")
    data_model.append(data_weather_attribute2)
    data_date_time_sat = DateTime(
        text="Saturday morning",
        value=datetime.now() + timedelta(days=((7 + 5 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_sat)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute1, date_time=data_date_time_sat
    )
    data_model.append(data_weather_forecast)

    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Ashley", value="Ashley Smith")
    data_model.append(data_recipient)
    data_content = Content(text="she wants to go for a hike")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("sunny")
    date_time = DateTime.resolve_from_text("Saturday morning")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("email")
        recipient = Contact.resolve_from_text("Ashley")
        content = Content.resolve_from_text("she wants to go for a hike")
        Messages.send_message(
            message_content_type=message_content_type,
            recipient=recipient,
            content=content,
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
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_63_b():
    """
    If the weather is going to be sunny Saturday morning, send an email to Ashley asking if she wants to go for a hike.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="cloudy")
    data_model.append(data_weather_attribute2)
    data_date_time_sat = DateTime(
        text="Saturday morning",
        value=datetime.now() + timedelta(days=((7 + 5 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_sat)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute2, date_time=data_date_time_sat
    )
    data_model.append(data_weather_forecast)

    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Ashley", value="Ashley Smith")
    data_model.append(data_recipient)
    data_content = Content(text="she wants to go for a hike")
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("sunny")
    date_time = DateTime.resolve_from_text("Saturday morning")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        message_content_type = MessageContentType.resolve_from_text("email")
        recipient = Contact.resolve_from_text("Ashley")
        content = Content.resolve_from_text("she wants to go for a hike")
        Messages.send_message(
            message_content_type=message_content_type,
            recipient=recipient,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_65():
    """
    Send a message to my friends list on Monday telling them to remember to vote and set a reminder to me too.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type = MessageContentType(text="a message")
    data_model.append(data_message_content_type)
    data_recipients = []
    for text, value in [
        ("my friends list", "Tom"),
        ("my friends list", "Jerry"),
        ("my friends list", "Mike"),
        ("my friends list", "Ashley"),
    ]:
        data_recipient = Contact(text=text, value=value)
        data_model.append(data_recipient)
        data_recipients.append(data_recipient)
    data_date_time_mon = DateTime(
        text="on Monday",
        value=datetime.now() + timedelta(days=((7 + 0 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_mon)
    data_content = Content(text="remember to vote")
    data_model.append(data_content)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)

    # start code block to test
    message_content_type = MessageContentType.resolve_from_text("a message")
    recipients = Contact.resolve_many_from_text("my friends list")
    date_time = DateTime.resolve_from_text("on Monday")
    content = Content.resolve_from_text("remember to vote")
    for recipient in recipients:
        Messages.send_message(
            recipient=recipient,
            content=content,
            date_time=date_time,
            message_content_type=message_content_type,
        )

    person_reminded = Contact.resolve_from_text("me")
    Reminders.create_reminder(person_reminded=person_reminded, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = list(
        map(
            lambda data_recipient: {
                "recipient": data_recipient,
                "content": data_content,
                "message_content_type": data_message_content_type,
            },
            data_recipients,
        )
    )
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [{"person_reminded": data_person_reminded, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_66():
    """
    Show me all of the musical events within 10 miles of me.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="all of the musical events")
    data_model.append(data_event_name)
    data_location = Location(text="within 10 miles of me")
    data_model.append(data_location)
    data_expected_events = []
    for _ in range(3):
        data_event = EventEntity(
            event_name=data_event_name,
            location=data_location,
        )
        data_model.append(data_event)
        data_expected_events.append(data_event)

    # start code block to test
    event_name = EventName.resolve_from_text(text="all of the musical events")
    location = Location.resolve_from_text(text="within 10 miles of me")
    events = Calendar.find_events(event_name=event_name, location=location)
    Responder.respond(response=events)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator)
    expected = data_expected_events
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_68():
    """
    Play my favorite music playlist and tell John I am running late and will be there soon.
    """
    # test data
    data_model = DataModel(reset=True)
    data_playlist = Playlist(text="my favorite music playlist")
    data_model.append(data_playlist)
    data_recipient = Contact(text="John")
    data_model.append(data_recipient)
    data_content = Content(text="I am running late and will be there soon")
    data_model.append(data_content)

    # start code block to test
    playlist = Playlist.resolve_from_text("my favorite music playlist")
    Music.play_music(playlist=playlist)

    recipient = Contact.resolve_from_text("John")
    content = Content.resolve_from_text("I am running late and will be there soon")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MusicEntity)
    expected = [{"playlist": data_playlist}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_70():
    """
    Look up current prices for Chicago Blackhawks tickets for tomorrow's game and tell me what the traffic conditions will be like around 5 PM
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="Chicago Blackhawks")
    data_model.append(data_event_name)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_event_ticket = EventTicketEntity(
        event_name=data_event_name, date_time=data_date_time_tomorrow
    )
    data_model.append(data_event_ticket)

    data_date_time_5pm = DateTime(text="5 PM", value=datetime.now().replace(hour=17))
    data_model.append(data_date_time_5pm)
    data_nav_traffic_info = NavigationTrafficInfoEntity(date_time=data_date_time_5pm)
    data_model.append(data_nav_traffic_info)

    # start code block to test
    event_name = EventName.resolve_from_text("Chicago Blackhawks")
    date_time = DateTime.resolve_from_text("tomorrow")
    event_tickets = Calendar.find_events_tickets(
        event_name=event_name, date_time=date_time
    )
    Responder.respond(response=event_tickets)

    date_time = DateTime.resolve_from_text("around 5 PM")
    navigation_traffic_info = Navigation.find_traffic_info(date_time=date_time)
    Responder.respond(response=navigation_traffic_info)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventTicketEntity]))
    actual = next(iterator)
    expected = [data_event_ticket]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationTrafficInfoEntity]))
    actual = next(iterator)
    expected = [data_nav_traffic_info]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_71():
    """
    Set timer to 30 mins and remind me to take the fish out of the oven.
    """
    # test data
    data_model = DataModel(reset=True)
    data_time_duration = TimeDuration(text="30 mins")
    data_model.append(data_time_duration)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="take the fish out of the oven")
    data_model.append(data_content)

    # start code block to test
    data_duration = TimeDuration.resolve_from_text("30 mins")
    Timer.create_timer(duration=data_duration)

    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("take the fish out of the oven")
    Reminders.create_reminder(person_reminded=person_reminded, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(TimerEntity)
    expected = [{"duration": data_time_duration}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [{"person_reminded": data_person_reminded, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_72_a():
    """
    Check the weather and if it's above 80 degrees, set a reminder on my calendar for "Go to the park later"
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_temperature1 = WeatherTemperature(text="above 80 degrees")
    data_model.append(data_weather_temperature1)
    data_weather_temperature2 = WeatherTemperature(text="79 degrees")
    data_model.append(data_weather_temperature2)
    data_weather_forecast = WeatherForecastEntity(
        weather_temperature=data_weather_temperature1
    )
    data_model.append(data_weather_forecast)
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_content = Content(text="Go to the park later")
    data_model.append(data_content)

    # start code block to test
    weather_forecasts = Weather.find_weather_forecasts()
    Responder.respond(response=weather_forecasts)

    weather_temperature = WeatherTemperature.resolve_from_text("above 80 degrees")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_temperature=weather_temperature
    )
    test_weather_forecast = bool(weather_forecasts)
    if test_weather_forecast:
        content = Content.resolve_from_text("Go to the park later")
        Reminders.create_reminder(content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [{"content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_72_b():
    """
    Check the weather and if it's above 80 degrees, set a reminder on my calendar for "Go to the park later"
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_temperature1 = WeatherTemperature(text="above 80 degrees")
    data_model.append(data_weather_temperature1)
    data_weather_temperature2 = WeatherTemperature(text="79 degrees")
    data_model.append(data_weather_temperature2)
    data_weather_forecast = WeatherForecastEntity(
        weather_temperature=data_weather_temperature2
    )
    data_model.append(data_weather_forecast)
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_content = Content(text="Go to the park later")
    data_model.append(data_content)

    # start code block to test
    weather_forecasts = Weather.find_weather_forecasts()
    Responder.respond(response=weather_forecasts)

    weather_temperature = WeatherTemperature.resolve_from_text("above 80 degrees")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_temperature=weather_temperature
    )
    test_weather_forecast = bool(weather_forecasts)
    if test_weather_forecast:
        content = Content.resolve_from_text("Go to the park later")
        Reminders.create_reminder(content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_73():
    """
    Remind me on Sunday about my doctor's appointment next Monday and give me directions to the doctor's office.
    """
    # test data
    data_model = DataModel(reset=True)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time_sunday = DateTime(
        text="on Sunday",
        value=datetime.now() + timedelta(days=((7 + 6 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_sunday)
    data_content = Content(text="my doctor's appointment next Monday")
    data_model.append(data_content)
    data_destination = Location(text="the doctor's office")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)

    # start code block to test
    person_reminded = Contact.resolve_from_text("me")
    date_time = DateTime.resolve_from_text("on Sunday")
    content = Content.resolve_from_text("my doctor's appointment next Monday")
    Reminders.create_reminder(
        person_reminded=person_reminded, date_time=date_time, content=content
    )

    destination = Location.resolve_from_text("the doctor's office")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_person_reminded,
            "date_time": data_date_time_sunday,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator)
    expected = [data_navigation_direction]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_75():
    """
    For Shakey Graves' upcoming summer tour, what will be the closest show to me and how many miles away is the venue?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="Shakey Graves' upcoming summer tour")
    data_model.append(data_event_name)
    data_event1 = EventEntity(event_name=data_event_name, closest=10)
    data_model.append(data_event1)
    data_event2 = EventEntity(event_name=data_event_name, closest=25)
    data_model.append(data_event2)
    data_event3 = EventEntity(event_name=data_event_name, closest=3)
    data_model.append(data_event3)
    data_destination = Location(value=data_event3)
    data_model.append(data_destination)
    data_navigation_distance = NavigationDistanceEntity(destination=data_destination)
    data_model.append(data_navigation_distance)

    # start code block to test
    event_name = EventName.resolve_from_text("Shakey Graves' upcoming summer tour")
    events = Calendar.find_events(event_name=event_name)
    events = utils.sort(events, "closest")
    event = utils.first(events)
    Responder.respond(response=event)

    destination = Location.resolve_from_entity(event)
    navigation_distances = Navigation.find_distance(destination=destination)
    Responder.respond(response=navigation_distances)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response(EventEntity))
    actual = next(iterator)
    expected = [data_event3]
    response_assertions(expected, [actual], test_results)

    iterator = iter(data_model.get_response([NavigationDistanceEntity]))
    actual = next(iterator)
    expected = [data_navigation_distance]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_76_a():
    """
    If is is raining at 8pm turn the heat up 5 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="clear blue sky")
    data_model.append(data_weather_attribute2)
    data_date_time = DateTime(
        text="8pm",
        value=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute1, date_time=data_date_time
        )
    )
    data_home_device_name = HomeDeviceName(text="the heat")
    data_model.append(data_home_device_name)
    data_home_device_action = HomeDeviceAction(text="turn")
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="up 5 degrees")
    data_model.append(data_home_device_value)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    date_time = DateTime.resolve_from_text("8pm")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        device_action = HomeDeviceAction.resolve_from_text("turn")
        device_name = HomeDeviceName.resolve_from_text("the heat")
        device_value = HomeDeviceValue.resolve_from_text("up 5 degrees")
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


def test_76_b():
    """
    If is is raining at 8pm turn the heat up 5 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute1 = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute1)
    data_weather_attribute2 = WeatherAttribute(text="clear blue sky")
    data_model.append(data_weather_attribute2)
    data_date_time = DateTime(
        text="8pm",
        value=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute2, date_time=data_date_time
        )
    )
    data_home_device_name = HomeDeviceName(text="the heat")
    data_model.append(data_home_device_name)
    data_home_device_action = HomeDeviceAction(text="turn")
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="up 5 degrees")
    data_model.append(data_home_device_value)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    date_time = DateTime.resolve_from_text("8pm")
    weather_forecasts = Weather.find_weather_forecasts(
        weather_attribute=weather_attribute, date_time=date_time
    )
    test_weather_forecasts = bool(weather_forecasts)
    if test_weather_forecasts:
        device_action = HomeDeviceAction.resolve_from_text("turn")
        device_name = HomeDeviceName.resolve_from_text("the heat")
        device_value = HomeDeviceValue.resolve_from_text("up 5 degrees")
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
