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
from actions.messages import *
from actions.music import *
from actions.navigation import *
from actions.reminders import *
from actions.responder import *
from actions.shopping import *
from actions.weather import *
from providers.data_model import DataModel
from datetime import datetime, timedelta
import utils
from tests.test_utils import *


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
    data_home_device_name = HomeDeviceName(
        text="the bedroom lights", value="the bedroom lights"
    )
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="turn on")
    data_model.append(data_home_device_value)
    data_date_time2 = DateTime(text="at 6 AM", value="at 6 AM")
    data_model.append(data_date_time2)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_alarms = data_model.get_data(AlarmEntity)
    assert_equal(len(data_alarms), 1, test_results)
    data_alarm = data_alarms[0]
    assert_equal(data_alarm.data.get("date_time"), data_date_time, test_results)

    data_alarms = data_model.get_data(HomeDeviceEntity)
    assert_equal(len(data_alarms), 1, test_results)
    data_alarm = data_alarms[0]
    assert_equal(
        data_alarm.data.get("device_action"), data_home_device_action, test_results
    )
    assert_equal(
        data_alarm.data.get("device_name"), data_home_device_name, test_results
    )
    assert_equal(
        data_alarm.data.get("device_value"), data_home_device_value, test_results
    )
    assert_equal(data_alarm.data.get("start_date_time"), data_date_time2, test_results)
    assert_test(test_results)


def test_25_a():
    """
    If the weather is nice tomorrow, text Jenny if she would like to go to the park
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="nice", value="nice")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(text="tomorrow", value="tomorrow")
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time, weather_attribute=data_weather_attribute
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
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
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
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 0, test_results)
    assert_test(test_results)


def test_27():
    """
    Send Tyler a text saying hi and send one to Susan too.
    """
    # test data
    data_model = DataModel(reset=True)
    data_tyler = Contact(text="Tyler", value="Tyler Durden")
    data_model.append(data_tyler)
    data_susan = Contact(text="Susan", value="Susan Sarandon")
    data_model.append(data_susan)
    data_content = Content(
        text="hi",
        value="hi",
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 2, test_results)
    assert_equal(data_messages[0].data.get("recipient"), data_tyler, test_results)
    assert_equal(data_messages[0].data.get("content"), data_content, test_results)
    assert_equal(data_messages[1].data.get("recipient"), data_susan, test_results)
    assert_equal(data_messages[1].data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_30():
    """
    Set timer for one hour labeled workout and start playing my music playlist titled workout tunes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_duration = DateTime(text="one hour", value=datetime.timedelta(hours=1))
    data_model.append(data_duration)
    data_playlist = Playlist(text="workout tunes", value="workout tunes")
    data_model.append(data_playlist)
    data_model.append(MusicEntity(playlist=data_playlist))

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_timers = data_model.get_data(TimerEntity)
    assert_equal(len(data_timers), 1, test_results)
    data_time = data_timers[0]
    assert_equal(data_time.data.get("duration"), data_duration, test_results)

    data_music_lists = data_model.get_data(MusicEntity)
    assert_equal(len(data_music_lists), 1, test_results)
    data_music = data_music_lists[0]
    assert_equal(data_music.data.get("playlist"), data_playlist, test_results)
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
    data_model.append(NavigationDirectionEntity(destination=data_destination))

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert_equal(len(data_home_devices), 1, test_results)
    data_home_device = data_home_devices[0]
    assert_equal(
        data_home_device.data.get("device_action"),
        data_home_device_action,
        test_results,
    )
    assert_equal(
        data_home_device.data.get("device_name"), data_home_device_name, test_results
    )
    assert_equal(
        data_home_device.data.get("device_value"), data_home_device_value, test_results
    )

    data_navigation_directions_lists = data_model.get_data(NavigationDirectionEntity)
    assert_equal(len(data_navigation_directions_lists), 1, test_results)
    data_navigation_directions = data_navigation_directions_lists[0]
    assert_equal(len(data_navigation_directions), 1, test_results)
    assert_equal(
        data_navigation_directions[0].data.get("destination"),
        data_destination,
        test_results,
    )
    assert_test(test_results)


def test_32():
    """
    Look up directions to the Sushi House and text my mom, telling her that I'm leaving soon
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination = Location(text="the Sushi House", value="the Sushi House")
    data_model.append(data_destination)
    data_model.append(NavigationDirectionEntity(destination=data_destination))
    data_recipient = Contact(text="my mom", value="my mom")
    data_model.append(data_recipient)
    data_content = Content(text="I'm leaving soon", value="I'm leaving soon")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_navigation_directions_lists = data_model.get_data(NavigationDirectionEntity)
    assert_equal(len(data_navigation_directions_lists), 1, test_results)
    data_navigation_directions = data_navigation_directions_lists[0]
    assert_equal(
        data_navigation_directions[0].data.get("destination"),
        data_destination,
        test_results,
    )

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_33():
    """
    Add eggs to my shopping list and text Steve to please buy eggs at the grocery store.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product = Product(text="eggs", value="eggs")
    data_model.append(data_product)
    data_model.append(ShoppingListEntity(products=[data_product]))
    data_recipient = Contact(text="Steve", value="Steven Smith")
    data_model.append(data_recipient)
    data_content = Content(
        text="please buy eggs at the grocery store",
        value="please buy eggs at the grocery store",
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_shopping_lists = data_model.get_data(ShoppingListEntity)
    assert_equal(len(data_shopping_lists), 1, test_results)
    data_shopping_list = data_shopping_lists[0]
    assert data_shopping_list.data.get("products").index(data_product) >= 0

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
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
        text="9am",
        value=datetime.now().replace(hour=7, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_alarm_date_time_9)
    data_model.append(AlarmEntity(date_time=data_alarm_date_time_9))

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_alarms = data_model.get_data(AlarmEntity)
    assert_equal(len(data_alarms), 1, test_results)
    data_alarm = data_alarms[0]
    assert_equal(data_alarm.data.get("date_time"), data_alarm_date_time_7, test_results)
    assert_test(test_results)


def test_35_b():
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
    data_model.append(AlarmEntity(date_time=data_alarm_date_time_9))

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_alarms = data_model.get_data(AlarmEntity)
    assert_equal(len(data_alarms), 1, test_results)
    data_alarm = data_alarms[0]
    assert_equal(data_alarm.data.get("date_time"), data_alarm_date_time_9, test_results)
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
    data_event_name = EventName(
        text="Jake's birthday party", value="Jake's birthday party"
    )
    data_model.append(data_event_name)
    data_recipient = Contact(text="Tom", value="Tom")
    data_model.append(data_recipient)
    data_content = Content(
        text="are you going to the party?", value="are you going to the party?"
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_events = data_model.get_data(EventEntity)
    assert_equal(len(data_events), 1, test_results)
    data_event = data_events[0]
    assert_equal(data_event.data.get("date_time"), data_date_time_sat7pm, test_results)
    assert_equal(data_event.data.get("event_name"), data_event_name, test_results)

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
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
    data_event_ticket = EventTicketEntity(event_name=data_event_name)
    data_content = Content(text="the pdf of the tickets", value=data_event_ticket)
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_event_tickets = data_model.get_data(EventTicketEntity)
    assert_equal(len(data_event_tickets), 1, test_results)
    data_event_ticket = data_event_tickets[0]
    assert_equal(
        data_event_ticket.data.get("event_name"), data_event_name, test_results
    )

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert (
        data_message.data.get("content")
        and data_message.data.get("content").data.get("event_name") == data_event_name
    )
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
    data_weather_attribute = WeatherAttribute(text="sunny", value="sun")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time_tomorrow, weather_attribute=data_weather_attribute
        )
    )
    data_recipient = Contact(text="my sister", value="my sister")
    data_model.append(data_recipient)
    data_content = Content(
        text="we should go out for lunch tomorrow",
        value="we should go out for lunch tomorrow",
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
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
    data_weather_attribute = WeatherAttribute(text="raining", value="rain")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time_tomorrow, weather_attribute=data_weather_attribute
        )
    )
    data_recipient = Contact(text="my sister", value="my sister")
    data_model.append(data_recipient)
    data_content = Content(
        text="we should go out for lunch tomorrow",
        value="we should go out for lunch tomorrow",
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 0, test_results)
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
    data_calendar = EventCalendar(text="my calendar", value="my calendar")
    data_model.append(data_calendar)
    data_event_name = EventName(text="dinner", value="dinner")
    data_model.append(
        EventEntity(
            date_time=data_date_time_19,
            calendar=data_calendar,
            event_name=data_event_name,
        )
    )
    data_recipient = Contact(text="Alice", value="Alice")
    data_model.append(data_recipient)
    data_content = Content(
        text="she wants to go dinner", value="do you want to go dinner"
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
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
    data_calendar = EventCalendar(text="my calendar", value="my calendar")
    data_model.append(data_calendar)
    data_event_name = EventName(text="dinner", value="dinner")
    data_model.append(
        EventEntity(
            date_time=data_date_time_20,
            calendar=data_calendar,
            event_name=data_event_name,
        )
    )
    data_recipient = Contact(text="Alice", value="Alice")
    data_model.append(data_recipient)
    data_content = Content(
        text="she wants to go dinner", value="do you want to go dinner"
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 0, test_results)
    assert_test(test_results)


def test_41():
    """
    Set the A/C to 72 degrees and set a timer for 30 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_action = HomeDeviceAction(text="set")
    data_model.append(data_home_device_action)
    data_home_device = HomeDeviceName(text="the A/C", value="A/C")
    data_model.append(data_home_device)
    data_home_device_value = HomeDeviceValue(text="72 degrees", value=72)
    data_model.append(data_home_device_value)
    data_date_time_30 = DateTime(
        text="30 minutes", value=datetime.now() + timedelta(minutes=30)
    )
    data_model.append(data_date_time_30)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert_equal(len(data_home_devices), 1, test_results)
    data_home_device = data_home_devices[0]
    assert_equal(
        data_home_device.data.get("device_action"),
        data_home_device_action,
        test_results,
    )
    assert_equal(
        data_home_device.data.get("device_name"), data_home_device, test_results
    )
    assert_equal(
        data_home_device.data.get("device_value"), data_home_device_value, test_results
    )
    data_timers = data_model.get_data(TimerEntity)
    assert_equal(len(data_timers), 1, test_results)
    data_timer = data_timers[0]
    assert_equal(data_timer.data.get("date_time"), data_date_time_30, test_results)
    assert_test(test_results)


def test_44():
    """
    Buy a ticket for the new Wakanda movie, What is Friday's weather going to be like?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(
        text="the new Wakanda movie", value="the new Wakanda movie"
    )
    data_model.append(data_event_name)
    data_event = EventEntity(event_name=data_event_name)
    data_model.append(data_event)
    data_date_time = DateTime(
        text="Friday",
        value=datetime.now() + timedelta(days=((7 + 4 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time)
    data_model.append(WeatherForecastEntity(date_time=data_date_time))

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_event_tickets = data_model.get_data(EventTicketEntity)
    assert_equal(len(data_event_tickets), 1, test_results)
    data_event_ticket = data_event_tickets[0]
    assert_equal(data_event_ticket.data.get("event"), data_event, test_results)

    data_weather_forecasts_list = data_model.get_data(WeatherForecastEntity)
    assert_equal(len(data_weather_forecasts_list), 1, test_results)
    data_weather_forecasts = data_weather_forecasts_list[0]
    assert_equal(len(data_weather_forecasts), 1, test_results)
    assert_equal(
        data_weather_forecasts[0].data.get("date_time"), data_date_time, test_results
    )
    assert_test(test_results)


def test_45():
    """
    Set a timer for 5 minutes and then when the timer is up send a message to Justin, telling him I am finished with the job.
    """
    # test data
    data_model = DataModel(reset=True)
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
    # end code block to test

    # assertions
    test_results = {}
    data_timers = data_model.get_data(TimerEntity)
    assert_equal(len(data_timers), 1, test_results)
    data_timer = data_timers[0]
    assert_equal(data_timer.data.get("date_time"), data_date_time_5m, test_results)

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
    assert_equal(data_message.data.get("date_time"), data_date_time_5m, test_results)
    assert_test(test_results)


def test_46():
    """
    Find the nearest In N Out and send a text to Bryan asking for his order.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location1 = Location(text="In N Out", value="In N Out branch #1", nearest=10)
    data_model.append(data_location1)
    data_location2 = Location(text="In N Out", value="In N Out branch #2", nearest=2)
    data_model.append(data_location2)
    data_location3 = Location(text="In N Out", value="In N Out branch #3", nearest=5)
    data_model.append(data_location3)
    data_recipient = Contact(text="Bryan", value="Bryan Adams")
    data_model.append(data_recipient)
    data_content = Content(text="his order", value="what is your order")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_map_entities = data_model.get_data(MapEntity)
    assert_equal(len(data_map_entities), 1, test_results)
    data_map_entity = data_map_entities[0]
    assert_equal(data_map_entity.data.get("location"), data_location2, test_results)

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
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
    data_home_device_name = HomeDeviceName(text="the thermostat", value="thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(
        text="turn up the temperature by 5 degrees", value=25
    )
    data_model.append(data_home_device_value)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_timers = data_model.get_data(TimerEntity)
    assert_equal(len(data_timers), 1, test_results)
    data_timer = data_timers[0]
    assert_equal(data_timer.data.get("date_time"), data_date_time_6am, test_results)

    data_home_devices = data_model.get_data(HomeDeviceValue)
    assert_equal(len(data_home_devices), 1, test_results)
    data_home_device = data_home_devices[0]
    assert_equal(
        data_home_device.data.get("device_name"), data_home_device_name, test_results
    )
    assert_equal(
        data_home_device.data.get("device_value"), data_home_device_value, test_results
    )
    assert_equal(
        data_home_device.data.get("date_time"), data_date_time_6am, test_results
    )
    assert_test(test_results)


def test_48():
    """
    Turn on the lights in the hallway at 7 pm and start playing my playlist at 8 pm.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_value = HomeDeviceValue(text="on", value="on")
    data_model.append(data_home_device_value)
    data_home_device_name = HomeDeviceName(
        text="the lights in the hallway", value="the lights in the hallway"
    )
    data_model.append(data_home_device_name)
    data_date_time_7pm = DateTime(
        text="7 pm", value=datetime.now().replace(hour=6, minute=0)
    )
    data_model.append(data_date_time_7pm)
    data_playlist = Playlist(text="my playlist", value="my playlist")
    data_model.append(data_playlist)
    data_date_time_8pm = DateTime(
        text="8 pm", value=datetime.now().replace(hour=8, minute=0)
    )
    data_model.append(data_date_time_8pm)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_home_devices = data_model.get_data(HomeDeviceValue)
    assert_equal(len(data_home_devices), 1, test_results)
    data_home_device = data_home_devices[0]
    assert_equal(
        data_home_device.data.get("device_name"), data_home_device_name, test_results
    )
    assert_equal(
        data_home_device.data.get("device_value"), data_home_device_value, test_results
    )
    assert_equal(
        data_home_device.data.get("date_time"), data_date_time_7pm, test_results
    )
    data_musics = data_model.get_data(MusicEntity)
    assert_equal(len(data_musics), 1, test_results)
    data_music = data_musics[0]
    assert_equal(data_music.data.get("playlist"), data_playlist, test_results)
    assert_equal(data_music.data.get("date_time"), data_date_time_8pm, test_results)
    assert_test(test_results)
