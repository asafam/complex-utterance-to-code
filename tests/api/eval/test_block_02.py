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
    response_assertions,
    assert_test,
    entity_assertions,
)


def test_22():
    """
    Set alarm for 6 AM and set the bedroom lights to turn on at 6 AM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="6 AM", value="6 AM")
    data_model.append(data_date_time)

    data_home_device_action = HomeDeviceAction(text="turn on", value="turn on")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the bedroom lights")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="turn on")
    data_model.append(data_home_device_value)
    data_date_time2 = DateTime(text="at 6 AM")
    data_model.append(data_date_time2)

    # start code block to test
    date_time = DateTime.resolve_from_text("6 AM")
    Alarm.create_alarm(date_time=date_time)

    device_name = HomeDeviceName.resolve_from_text("the bedroom lights")
    device_action = HomeDeviceAction.resolve_from_text("turn on")
    device_value = HomeDeviceValue.resolve_from_text("turn on")
    date_time = DateTime.resolve_from_text("at 6 AM")
    SmartHome.execute_home_device_action(
        date_time=date_time,
        device_name=device_name,
        device_action=device_action,
        device_value=device_value,
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [{"date_time": data_date_time}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_name": data_home_device_name,
            "device_action": data_home_device_action,
            "device_value": data_home_device_value,
            "date_time": data_date_time2,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_25_a():
    """
    If the weather is nice tomorrow, text Jenny if she would like to go to the park
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="nice")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(text="tomorrow")
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time, weather_attribute=data_weather_attribute
        )
    )
    data_recipient = Contact(text="Jenny")
    data_model.append(data_recipient)
    data_content = Content(
        text="if she would like to go to the park",
    )
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_attribute = WeatherAttribute.resolve_from_text("nice")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    test_weather = bool(weather_forecasts)
    if test_weather:
        recipient = Contact.resolve_from_text("Jenny")
        content = Content.resolve_from_text("if she would like to go to the park")
        Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_25_b():
    """
    If the weather is nice tomorrow, text Jenny if she would like to go to the park
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="nice", value="nice")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="stormy", value="storm")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(text="tomorrow", value="tomorrow")
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time, weather_attribute=data_weather_attribute_neg
        )
    )
    data_recipient = Contact(text="Jenny", value="Jennifer Lopez")
    data_model.append(data_recipient)
    data_content = Content(
        text="if she would like to go to the park",
        value="if she would like to go to the park",
    )
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_attribute = WeatherAttribute.resolve_from_text("nice")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    test_weather = bool(weather_forecasts)
    if test_weather:
        recipient = Contact.resolve_from_text("Jenny")
        content = Content.resolve_from_text("if she would like to go to the park")
        Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_27():
    """
    Send Tyler a text saying hi and send one to Susan too.
    """
    # test data
    data_model = DataModel(reset=True)
    data_tyler = Contact(text="Tyler")
    data_model.append(data_tyler)
    data_susan = Contact(text="Susan")
    data_model.append(data_susan)
    data_content = Content(
        text="hi",
    )
    data_model.append(data_content)

    # start code block to test
    recipient = Contact.resolve_from_text("Tyler")
    content = Content.resolve_from_text("hi")
    Messages.send_message(recipient=recipient, content=content)

    recipient = Contact.resolve_from_text("Susan")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [
        {"recipient": data_tyler, "content": data_content},
        {"recipient": data_susan, "content": data_content},
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_30():
    """
    Set timer for one hour labeled workout and start playing my music playlist titled workout tunes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_duration = TimeDuration(text="one hour")
    data_model.append(data_duration)
    data_playlist = Playlist(text="workout tunes")
    data_model.append(data_playlist)

    # start code block to test
    duration = TimeDuration.resolve_from_text("one hour")
    Timer.create_timer(duration=duration)

    playlist = Playlist.resolve_from_text("workout tunes")
    Music.play_music(playlist=playlist)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(TimerEntity)
    expected = [{"duration": data_duration}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MusicEntity)
    expected = [{"playlist": data_playlist}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_31():
    """
    Turn on the living room lights and navigate Home.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_action = HomeDeviceAction(text="Turn")
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="on", value="on")
    data_model.append(data_home_device_value)
    data_home_device_name = HomeDeviceName(
        text="the living room lights", value="the living room lights"
    )
    data_model.append(data_home_device_name)
    data_destination = Location(text="Home", value="Home")
    data_model.append(data_destination)
    data_navigation_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_navigation_direction)

    # start code block to test
    home_device_action = HomeDeviceAction.resolve_from_text("Turn")
    home_device_value = HomeDeviceValue.resolve_from_text("on")
    home_device_name = HomeDeviceName.resolve_from_text("the living room lights")
    SmartHome.execute_home_device_action(
        device_name=home_device_name,
        device_action=home_device_action,
        device_value=home_device_value,
    )

    destination = Location.resolve_from_text("Home")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)
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

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_direction]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_32():
    """
    Look up directions to the Sushi House and text my mom, telling her that I'm leaving soon
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination = Location(text="the Sushi House", value="the Sushi House")
    data_model.append(data_destination)
    data_directions = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_directions)
    data_recipient = Contact(text="my mom")
    data_model.append(data_recipient)
    data_content = Content(text="I'm leaving soon")
    data_model.append(data_content)

    # start code block to test
    destination = Location.resolve_from_text("the Sushi House")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)

    recipient = Contact.resolve_from_text("my mom")
    content = Content.resolve_from_text("I'm leaving soon")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_directions]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_33():
    """
    Add eggs to my shopping list and text Steve to please buy eggs at the grocery store.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name = ProductName(text="eggs")
    data_model.append(data_product_name)
    data_shopping_list_name = ShoppingListName(text="my shopping list")
    data_model.append(data_shopping_list_name)
    data_recipient = Contact(text="Steve")
    data_model.append(data_recipient)
    data_content = Content(text="please buy eggs at the grocery store")
    data_model.append(data_content)

    # start code block to test
    product_name = ProductName.resolve_from_text("eggs")
    shopping_list_name = ShoppingListName.resolve_from_text("my shopping list")
    Shopping.add_to_shopping_list(
        product_name=product_name, shopping_list_name=shopping_list_name
    )

    recipient = Contact.resolve_from_text("Steve")
    content = Content.resolve_from_text("please buy eggs at the grocery store")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ShoppingListEntity)
    expected = [
        {
            "product_name": data_product_name,
            "shopping_list_name": data_shopping_list_name,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_35_a():
    """
    If I receive a text from Ruby tonight, change my alarm to 7am.
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender_ruby = Contact(text="Ruby", value="Ruby Chen")
    data_model.append(data_sender_ruby)
    data_sender_steve = Contact(text="Steve", value="Steven Smith")
    data_model.append(data_sender_steve)
    data_date_time_tonight = DateTime(text="tonight", value=datetime.now())
    data_model.append(data_date_time_tonight)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_model.append(
        MessageEntity(sender=data_sender_ruby, date_time=data_date_time_tonight)
    )
    data_model.append(
        MessageEntity(sender=data_sender_ruby, date_time=data_date_time_tomorrow)
    )
    data_model.append(
        MessageEntity(sender=data_sender_steve, date_time=data_date_time_tonight)
    )
    data_alarm_date_time_9 = DateTime(
        text="9am",
        value=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_alarm_date_time_9)
    data_alarm_date_time_7 = DateTime(
        text="7am",
        value=datetime.now().replace(hour=7, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_alarm_date_time_7)
    data_alarm_name = AlarmName(text="my alarm")
    data_model.append(data_alarm_name)

    # start code block to test
    sender = Contact.resolve_from_text("Ruby")
    date_time = DateTime.resolve_from_text("tonight")
    messages = Messages.find_messages(sender=sender, date_time=date_time)
    test_messages = bool(messages)
    if test_messages:
        alarm_name = AlarmName.resolve_from_text("my alarm")
        date_time = DateTime.resolve_from_text("7am")
        Alarm.update_alarm(alarm_name=alarm_name, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = [{"alarm_name": data_alarm_name, "date_time": data_alarm_date_time_7}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_35_b():
    """
    If I receive a text from Ruby tonight, change my alarm to 7am.
    """
    # test data
    data_model = DataModel(reset=True)
    data_sender_ruby = Contact(text="Ruby")
    data_model.append(data_sender_ruby)
    data_sender_steve = Contact(text="Steve")
    data_model.append(data_sender_steve)
    data_date_time_tonight = DateTime(text="tonight")
    data_model.append(data_date_time_tonight)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_model.append(
        MessageEntity(sender=data_sender_ruby, date_time=data_date_time_tomorrow)
    )
    data_model.append(
        MessageEntity(sender=data_sender_steve, date_time=data_date_time_tonight)
    )
    data_alarm_date_time_9 = DateTime(
        text="9am",
        value=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_alarm_date_time_9)

    # start code block to test
    sender = Contact.resolve_from_text("Ruby")
    date_time = DateTime.resolve_from_text("tonight")
    messages = Messages.find_messages(sender=sender, date_time=date_time)
    test_messages = bool(messages)
    if test_messages:
        alarm_name = AlarmName.resolve_from_text("my alarm")
        date_time = DateTime.resolve_from_text("7am")
        Alarm.update_alarm(alarm_name=alarm_name, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(AlarmEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_36():
    """
    Add Jake's birthday party to the calendar for 7pm Saturday then send an email to Tom are you going to the party?
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_sat7pm = DateTime(
        text="7pm Saturday",
        value=(
            datetime.now()
            + timedelta(
                days=((12 - datetime.now().weekday()) % 7)
            )  # find next Sat https://stackoverflow.com/a/16770463/1609802
        ).replace(hour=19, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time_sat7pm)
    data_event_name = EventName(text="Jake's birthday party")
    data_model.append(data_event_name)
    data_recipient = Contact(text="Tom")
    data_model.append(data_recipient)
    data_content = Content(text="are you going to the party?")
    data_model.append(data_content)

    # start code block to test
    event_name = EventName.resolve_from_text("Jake's birthday party")
    date_time = DateTime.resolve_from_text("7pm Saturday")
    Calendar.schedule_event(event_name=event_name, date_time=date_time)

    recipient = Contact.resolve_from_text("Tom")
    content = Content.resolve_from_text("are you going to the party?")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventEntity)
    expected = [{"event_name": data_event_name, "date_time": data_date_time_sat7pm}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_38():
    """
    Buy tickets to Black Adam and email the pdf of the tickets to Carlos.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="Black Adam", value="Black Adam")
    data_model.append(data_event_name)
    data_recipient = Contact(text="Carlos", value="Carlos")
    data_model.append(data_recipient)
    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)

    # start code block to test
    event_name = EventName.resolve_from_text("Black Adam")
    tickets = Calendar.purchase_tickets(event_name=event_name)

    message_content_type = MessageContentType.resolve_from_text("email")
    recipient = Contact.resolve_from_text("Carlos")
    content = Content.resolve_from_entity(tickets)
    Messages.send_message(
        recipient=recipient, content=content, message_content_type=message_content_type
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventTicketEntity)
    expected = [{"event_name": data_event_name}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": Content(value=ticket),
            "message_content_type": message_content_type,
        }
        for ticket in data_model.get_data(EventTicketEntity)
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_39_a():
    """
    Look up what the weather will be like tomorrow, if it's not raining, message my sister saying we should go out for lunch tomorrow.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_weather_attribute = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute)
    data_weather_attribute_raining = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute_raining)
    data_weather_forecast = WeatherForecastEntity(
        date_time=data_date_time_tomorrow, weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast)
    data_message_content_type = MessageContentType(text="message")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="my sister")
    data_model.append(data_recipient)
    data_content = Content(
        text="we should go out for lunch tomorrow",
    )
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_attribute=weather_attribute
    )
    test_weather = bool(weather_forecasts)
    if not test_weather:
        message_content_type = MessageContentType.resolve_from_text("message")
        recipient = Contact.resolve_from_text("my sister")
        content = Content.resolve_from_text("we should go out for lunch tomorrow")
        Messages.send_message(
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_39_b():
    """
    Look up what the weather will be like tomorrow, if it's not raining, message my sister saying we should go out for lunch tomorrow.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_weather_forecast = WeatherForecastEntity(
        date_time=data_date_time_tomorrow, weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast)
    data_message_content_type = MessageContentType(text="message")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="my sister")
    data_model.append(data_recipient)
    data_content = Content(
        text="we should go out for lunch tomorrow",
    )
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_attribute=weather_attribute
    )
    test_weather = bool(weather_forecasts)
    if not test_weather:
        message_content_type = MessageContentType.resolve_from_text("message")
        recipient = Contact.resolve_from_text("my sister")
        content = Content.resolve_from_text("we should go out for lunch tomorrow")
        Messages.send_message(
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
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


def test_40_a():
    """
    If I don't have anything scheduled on the 20th of this month on my calendar, message Alice and ask if she wants to go dinner.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_20 = DateTime(
        text="20th of this month", value=datetime.now().replace(day=20)
    )
    data_model.append(data_date_time_20)
    data_date_time_19 = DateTime(
        text="19th of this month", value=datetime.now().replace(day=19)
    )
    data_model.append(data_date_time_19)
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_event_name = EventName(text="dinner")
    data_model.append(
        EventEntity(
            date_time=data_date_time_19,
            event_calendar=data_calendar,
            event_name=data_event_name,
        )
    )
    data_recipient = Contact(text="Alice")
    data_model.append(data_recipient)
    data_content = Content(text="she wants to go dinner")
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("20th of this month")
    event_calendar = EventCalendar.resolve_from_text("my calendar")
    events = Calendar.find_events(date_time=date_time, event_calendar=event_calendar)
    test_events = bool(events)
    if not test_events:
        recipient = Contact.resolve_from_text("Alice")
        content = Content.resolve_from_text("she wants to go dinner")
        Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_40_b():
    """
    If I don't have anything scheduled on the 20th of this month on my calendar, message Alice and ask if she wants to go dinner.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_20 = DateTime(
        text="20th of this month", value=datetime.now().replace(day=20)
    )
    data_model.append(data_date_time_20)
    data_date_time_19 = DateTime(
        text="19th of this month", value=datetime.now().replace(day=19)
    )
    data_model.append(data_date_time_19)
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_event_name = EventName(text="dinner")
    data_model.append(
        EventEntity(
            date_time=data_date_time_20,
            event_calendar=data_calendar,
            event_name=data_event_name,
        )
    )
    data_recipient = Contact(text="Alice")
    data_model.append(data_recipient)
    data_content = Content(text="she wants to go dinner")
    data_model.append(data_content)

    # start code block to test
    date_time = DateTime.resolve_from_text("20th of this month")
    event_calendar = EventCalendar.resolve_from_text("my calendar")
    events = Calendar.find_events(date_time=date_time, event_calendar=event_calendar)
    test_events = bool(events)
    if not test_events:
        recipient = Contact.resolve_from_text("Alice")
        content = Content.resolve_from_text("she wants to go dinner")
        Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_41():
    """
    Set the A/C to 72 degrees and set a timer for 30 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_action = HomeDeviceAction(text="set")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the A/C", value="A/C")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="72 degrees", value=72)
    data_model.append(data_home_device_value)
    data_duration_30 = TimeDuration(text="30 minutes")
    data_model.append(data_duration_30)

    # start code block to test
    device_action = HomeDeviceAction.resolve_from_text("set")
    device_name = HomeDeviceName.resolve_from_text("the A/C")
    device_value = HomeDeviceValue.resolve_from_text("72 degrees")
    SmartHome.execute_home_device_action(
        device_name=device_name, device_action=device_action, device_value=device_value
    )

    duration = TimeDuration.resolve_from_text("30 minutes")
    Timer.create_timer(duration=duration)

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

    actual = data_model.get_data(TimerEntity)
    expected = [{"duration": data_duration_30}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_44():
    """
    Buy a ticket for the new Wakanda movie, What is Friday's weather going to be like?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="the new Wakanda movie")
    data_model.append(data_event_name)
    data_date_time = DateTime(
        text="Friday",
        value=datetime.now() + timedelta(days=((7 + 4 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time)
    data_weather_forecast = WeatherForecastEntity(date_time=data_date_time)
    data_model.append(data_weather_forecast)

    # start code block to test
    event_name = EventName.resolve_from_text("the new Wakanda movie")
    Calendar.purchase_tickets(event_name=event_name)

    date_time = DateTime.resolve_from_text("Friday")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(EventTicketEntity)
    expected = [{"event_name": data_event_name}]
    entity_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_45():
    """
    Set a timer for 5 minutes and then when the timer is up send a message to Justin, telling him I am finished with the job.
    """
    # test data
    data_model = DataModel(reset=True)
    data_duration = TimeDuration(text="5 minutes")
    data_model.append(data_duration)
    data_date_time_5m = DateTime(
        text="5 minutes", value=datetime.now() + timedelta(minutes=5)
    )
    data_model.append(data_date_time_5m)
    data_recipient = Contact(text="Justin", value="Justin Bieber")
    data_model.append(data_recipient)
    data_content = Content(
        text="I am finished with the job", value="I am finished with the job"
    )
    data_model.append(data_content)

    # start code block to test
    duration = TimeDuration.resolve_from_text("5 minutes")
    Timer.create_timer(duration=duration)

    date_time = DateTime.resolve_from_text("5 minutes")
    contact = Contact.resolve_from_text("Justin")
    content = Content.resolve_from_text("I am finished with the job")
    Messages.send_message(recipient=contact, content=content, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(TimerEntity)
    expected = [{"duration": data_duration}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": data_content,
            "date_time": data_date_time_5m,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_46():
    """
    Find the nearest In N Out and send a text to Bryan asking for his order.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location1 = Location(text="In N Out", nearest=10)
    data_model.append(data_location1)
    data_location2 = Location(text="In N Out", nearest=2)
    data_model.append(data_location2)
    data_location3 = Location(text="In N Out", nearest=5)
    data_model.append(data_location3)
    data_map_entity1 = MapEntity(location=data_location1)
    data_model.append(data_map_entity1)
    data_map_entity2 = MapEntity(location=data_location2)
    data_model.append(data_map_entity2)
    data_map_entity3 = MapEntity(location=data_location3)
    data_model.append(data_map_entity3)
    data_recipient = Contact(text="Bryan")
    data_model.append(data_recipient)
    data_content = Content(text="his order")
    data_model.append(data_content)

    # start code block to test
    locations = Location.resolve_many_from_text("In N Out")
    locations = utils.sort(locations, "nearest")
    location = utils.first(locations)
    map_entities = Map.find_on_map(location=location)
    Responder.respond(response=map_entities)

    recipient = Contact.resolve_from_text("Bryan")
    content = Content.resolve_from_text("his order")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([MapEntity]))
    actual = next(iterator, None)
    expected = [data_map_entity2]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_47():
    """
    Set a timer for 6 AM to wake up, also set the thermostat to turn up the temperature by 5 degrees at 6 AM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_6am = DateTime(
        text="6 AM", value=datetime.now().replace(hour=6, minute=0)
    )
    data_model.append(data_date_time_6am)
    data_home_device_name = HomeDeviceName(
        text="the thermostat",
    )
    data_model.append(data_home_device_name)
    data_home_device_action = HomeDeviceAction(
        text="turn up the temperature",
    )
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="by 5 degrees", value=25)
    data_model.append(data_home_device_value)

    # start code block to test
    date_time = DateTime.resolve_from_text("6 AM")
    Timer.create_timer(date_time=date_time)

    device_name = HomeDeviceName.resolve_from_text("the thermostat")
    device_action = HomeDeviceAction.resolve_from_text("turn up the temperature")
    device_value = HomeDeviceValue.resolve_from_text("by 5 degrees")
    SmartHome.execute_home_device_action(
        device_name=device_name, device_action=device_action, device_value=device_value
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(TimerEntity)
    expected = [{"date_time": data_date_time_6am}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_name": data_home_device_name,
            "device_value": data_home_device_value,
            "device_action": data_home_device_action,
        }
    ]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_48():
    """
    Turn on the lights in the hallway at 7 pm and start playing my playlist at 8 pm.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_action = HomeDeviceAction(text="turn on")
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="on")
    data_model.append(data_home_device_value)
    data_home_device_name = HomeDeviceName(text="the lights in the hallway")
    data_model.append(data_home_device_name)
    data_date_time_7pm = DateTime(
        text="at 7 pm", value=datetime.now().replace(hour=6, minute=0)
    )
    data_model.append(data_date_time_7pm)
    data_playlist = Playlist(text="my playlist")
    data_model.append(data_playlist)
    data_date_time_8pm = DateTime(
        text="at 8 pm", value=datetime.now().replace(hour=8, minute=0)
    )
    data_model.append(data_date_time_8pm)

    # start code block to test
    device_name = HomeDeviceName.resolve_from_text("the lights in the hallway")
    device_action = HomeDeviceAction.resolve_from_text("turn on")
    device_value = HomeDeviceValue.resolve_from_text("on")
    date_time = DateTime.resolve_from_text("at 7 pm")
    SmartHome.execute_home_device_action(
        device_name=device_name,
        device_action=device_action,
        device_value=device_value,
        date_time=date_time,
    )

    playlist = Playlist.resolve_from_text("my playlist")
    date_time = DateTime.resolve_from_text("at 8 pm")
    Music.play_music(playlist=playlist, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(HomeDeviceEntity)
    expected = [
        {
            "device_name": data_home_device_name,
            "device_action": data_home_device_action,
            "device_value": data_home_device_value,
            "date_time": data_date_time_7pm,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MusicEntity)
    expected = [{"playlist": data_playlist, "date_time": data_date_time_8pm}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)
