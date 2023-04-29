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
from actions.calendar import Calendar
from actions.clock import *
from actions.calendar import *
from actions.home import *
from actions.map import Map
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
from tests.test_utils import *


def test_78_a():
    """
    If I get a text message from my boss Tony, then check my mail to see if I have any emails from work.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type_text = MessageContentType(text="text message")
    data_model.append(data_message_content_type_text)
    data_sender_boss = Contact(text="my boss Tony")
    data_model.append(data_sender_boss)
    data_model.append(
        MessageEntity(
            content_type=data_message_content_type_email, sender=data_sender_boss
        )
    )
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type_email = MessageContentType(text="emails")
    data_model.append(data_message_content_type_email)
    data_sender_work = Contact(text="work")
    data_model.append(data_sender_work)
    data_model.append(
        MessageEntity(
            sender=data_sender_work,
            recipient=data_recipient,
            content_type=data_message_content_type_email,
        )
    )
    data_model.append(
        MessageEntity(
            sender=data_sender_work,
            recipient=data_recipient,
            content_type=data_message_content_type_email,
        )
    )
    
    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 2
    for i in range(len(data_messages)):
        assert test_equal(data_messages[0].data.get("sender"), data_sender_work)
        assert test_equal(data_messages[i].data.get("recipient"), data_recipient)
        assert test_equal(
            data_messages[i].data.get("content_type"), data_message_content_type_email
        )


def test_78_a():
    """
    If I get a text message from my boss Tony, then check my mail to see if I have any emails from work.
    """
    # test data
    data_model = DataModel(reset=True)
    data_message_content_type_text = MessageContentType(text="text message")
    data_model.append(data_message_content_type_text)
    data_sender_boss = Contact(text="my boss Tony")
    data_model.append(data_sender_boss)
    data_sender_neg = Contact(text="not my boss Tony")
    data_model.append(
        MessageEntity(
            content_type=data_message_content_type_email, sender=data_sender_neg
        )
    )
    data_recipient = Contact(text="I")
    data_model.append(data_recipient)
    data_message_content_type_email = MessageContentType(text="emails")
    data_model.append(data_message_content_type_email)
    data_sender_work = Contact(text="work")
    data_model.append(data_sender_work)
    data_model.append(
        MessageEntity(
            sender=data_sender_work,
            recipient=data_recipient,
            content_type=data_message_content_type_email,
        )
    )
    data_model.append(
        MessageEntity(
            sender=data_sender_work,
            recipient=data_recipient,
            content_type=data_message_content_type_email,
        )
    )
    
    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 0


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
    data_weather_temperature = WeatherTemperature(text="above 90 degrees")
    data_model.append(data_weather_temperature)
    data_model.append(data_date_time_tuesday)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time_tuesday, temperature=data_weather_temperature
        )
    )
    data_content = Content(text="beach day")
    data_model.append(data_content)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)
    
    # start code block to test
    # end code block to test

    # assertions
    data_events = data_model.get_data(EventEntity)
    assert len(data_events) == 1
    data_event = data_events[0]
    assert test_equal(data_event.data.get("content"), data_content)
    assert test_equal(data_event.data.get("calendar"), data_event_calendar)


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
    data_weather_temperature = WeatherTemperature(text="above 90 degrees")
    data_model.append(data_weather_temperature)
    data_model.append(data_date_time_tuesday)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time_tuesday, temperature=data_weather_temperature
        )
    )
    data_content = Content(text="beach day")
    data_model.append(data_content)
    data_event_calendar = EventCalendar(text="my calendar")
    data_model.append(data_event_calendar)
    
    # start code block to test
    # end code block to test

    # assertions
    data_events = data_model.get_data(EventEntity)
    assert len(data_events) == 0


def test_80():
    """
    Message my brother I will not be able to make it to his house for dinner because of a flat tire, also look up tire repair places nearby.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="my brother")
    data_model.append(data_recipient)
    data_content = Content(
        text="I will not be able to make it to his house for dinner because of a flat tire"
    )
    data_model.append(data_content)
    data_location = Location(text="tire repair places")
    data_model.append(data_location)

    data_model.append(MapEntity(location=data_location, nearby=1))
    
    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert test_equal(data_message.data.get("recipient"), data_recipient)
    assert test_equal(data_message.data.get("content"), data_content)


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
        text="8:00 PM",
        value=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time_8pm)
    
    # start code block to test
    # end code block to test

    # assertions
    data_timers = data_model.get_data(TimerEntity)
    assert len(data_timers) == 0
    data_timer = data_timers[0]
    assert test_equal(data_timer.data.get("date_time"), data_date_time_3pm)

    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert len(data_home_devices) == 1
    data_home_device = data_home_devices[0]
    assert test_equal(
        data_home_device.data.get("device_action"), data_home_device_action
    )
    assert test_equal(data_home_device.data.get("device_name"), data_home_device_name)
    assert test_equal(data_home_device.data.get("device_value"), data_home_device_value)
    assert test_equal(data_home_device.data.get("end_date_time"), data_date_time_8pm)


def test_85_a():
    """
    If it starts raining between 3pm-5pm, turn the thermostat up to 73 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(
        text="3pm-5pm",
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
    data_home_device_name = HomeDeviceName(text="thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="73 degrees")
    data_model.append(data_home_device_value)
    
    # start code block to test
    # end code block to test

    # assertions
    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert len(data_home_devices) == 1
    data_home_device = data_home_devices[0]
    assert test_equal(
        data_home_device.data.get("device_action"), data_home_device_action
    )
    assert test_equal(data_home_device.data.get("device_name"), data_home_device_name)
    assert test_equal(data_home_device.data.get("device_value"), data_home_device_value)


def test_85_b():
    """
    If it starts raining between 3pm-5pm, turn the thermostat up to 73 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(
        text="3pm-5pm",
        value=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_date_time_neg = DateTime(
        text="6pm",
        value=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
    )
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time_neg
        )
    )
    data_home_device_action = HomeDeviceAction(text="turn")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="73 degrees")
    data_model.append(data_home_device_value)
    
    # start code block to test
    # end code block to test

    # assertions
    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert len(data_home_devices) == 0


def test_86():
    """
    Show me a map of downtown Phoenix and give me directions to the airport.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="downtown Phoenix")
    data_model.append(data_location)
    data_model.append(MapEntity(location=data_location))
    data_destination = Location(text="airport")
    data_model.append(data_destination)
    data_model.append(NavigationDirectionEntity(destination=data_destination))
    
    # start code block to test
    # end code block to test

    # assertions
    data_map_locations_lists = data_model.get_data(MapEntity)
    assert len(data_map_locations_lists) == 1
    data_map_locations = data_map_locations_lists[0]
    assert len(data_map_locations) == 1
    assert test_equal(data_map_locations[0].data.get("location"), data_location)

    data_navigation_directions_lists = data_model.get_data(NavigationDirectionEntity)
    assert len(data_navigation_directions_lists) == 1
    data_navigation_directions = data_navigation_directions_lists[0]
    assert test_equal(
        data_navigation_directions[0].data.get("destination"), data_destination
    )


def test_87():
    """
    Play my lofi Spotify playlist and buy tickets to the upcoming Joji show.
    """
    # test data
    data_model = DataModel(reset=True)
    data_playlist = Playlist(text="lofi Spotify playlist")
    data_model.append(data_playlist)
    data_event_name = EventName(text="Joji show")
    data_model.append(data_event_name)
    data_events = []
    for i in range(3):
        data_event = EventEntity(
            playlist=data_playlist, upcoming=datetime.now() + timedelta(days=i)
        )
        data_events.append(data_event)
        data_model.append(EventTicketEntity(event=data_event))
    data_event_upcoming = sorted(data_events, key=lambda x: x.data.get("upcoming"))[0]
    
    # start code block to test
    # end code block to test

    # assertions
    data_musics = data_model.get_data(NavigationDirectionEntity)
    assert len(data_musics) == 1
    data_music = data_musics[0]
    assert test_equal(data_music.data.get("playlist"), data_playlist)

    data_event_tickets = data_model.get_data(EventTicketEntity)
    assert len(data_event_tickets) == 1
    data_event_ticket = data_event_tickets[0]
    assert test_equal(data_event_ticket.data.get("event"), data_event_upcoming
    assert test_equal(
        data_event_ticket.data.get("event").data.get("event_name"),
        data_event_name,
    )


def test_88_a():
    """
    Check if it's supposed to rain tonight and if it's not text Brian that I want to go out tonight
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_date_time = DateTime(text="tonight")
    data_model.append(data_date_time)
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute_neg))
    data_contact_brian = Contact(text="Brian")
    data_model.append(data_contact_brian)
    data_content = Content(text="I want to go out tonight")
    data_model.append(data_content)
    
    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert test_equal(data_message.data.get("contact"), data_contact_brian)
    
    
def test_88_b():
    """
    Check if it's supposed to rain tonight and if it's not text Brian that I want to go out tonight
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_date_time = DateTime(text="tonight")
    data_model.append(data_date_time)
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute))
    data_contact_brian = Contact(text="Brian")
    data_model.append(data_contact_brian)
    data_content = Content(text="I want to go out tonight")
    data_model.append(data_content)
    
    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 0


def test_92():
    """
    Look up free events for this weekend and let me know what the weather will be.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="free events")
    data_model.append(data_event_name)
    data_date_time1 = DateTime(text="this weekend", value=datetime.now() + timedelta(days=0)) 
    data_model.append(data_date_time1)
    data_date_time2 = DateTime(text="this weekend", value=datetime.now() + timedelta(days=0))
    data_model.append(data_date_time2)
    data_date_times = [data_date_time1, data_date_time2]
    data_model.append(EventEntity(event_name=data_event_name, date_time=data_date_time1))
    data_model.append(EventEntity(event_name=data_event_name, date_time=data_date_time2))
    data_model.append(EventEntity(event_name=data_event_name, date_time=data_date_time2))
    data_model.append(WeatherForecastEntity(date_time=data_date_time1))
    data_model.append(WeatherForecastEntity(date_time=data_date_time2))
    
    # start code block to test
    # end code block to test
    
    # assertions
    data_events = data_model.get_data(EventEntity)
    assert len(data_events) == 3
    for data_date_time in data_date_times:
        assert filter(
            lambda data_event: test_equal(
                data_event.data.get("event_name"), data_event_name)
                and test_equal(data_event.data.get("date_time"), data_date_time),
            data_messages,
        )
    data_weather_forecasts_lists = data_model.get_data(WeatherForecastEntity)
    assert len(data_weather_forecasts_lists) == 2
    data_weather_forecasts = data_weather_forecasts_lists[0]
    for data_date_time in data_date_times:
        assert filter(
            lambda data_weather_forecast: test_equal(data_weather_forecast.data.get("date_time"), data_date_time),
            data_weather_forecasts
        )
          


def test_94_a():
    """
    When rain is forecasted for tomorrow? remind me at 9pm the night before to put out Quinten's boots by the front door.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_date_time_tomorrow = DateTime(
        text="tomorrow", 
        value=(datetime.now() + deltatime(days=1)).replace(hour=0 minute=0, second=0, microsecond=0)
    )
    data_model.append(data_date_time_tomorrow)
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute, date_time=data_date_time))
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute_neg, date_time=data_date_time))
    data_date_time_9pm = DateTime(
        text="9pm the night before", 
        value=data_date_time_tomorrow
    )
    data_model.append(data_date_time_9pm)
    data_content = Content(text="put out Quinten's boots by the front door")
    data_model.append(data_content)
    
    # start code block to test
    # end code block to test
    
    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert test_equal(data_reminder.data.get("date_time"), data_date_time_9pm)
    assert test_equal(data_reminder.data.get("content"), data_content)
    
    
def test_94_b():
    """
    When rain is forecasted for tomorrow? remind me at 9pm the night before to put out Quinten's boots by the front door.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not rain")
    data_date_time_tomorrow = DateTime(
        text="tomorrow", 
        value=(datetime.now() + deltatime(days=1)).replace(hour=0 minute=0, second=0, microsecond=0)
    )
    data_model.append(data_date_time_tomorrow)
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute_neg, date_time=data_date_time))
    data_date_time_9pm = DateTime(
        text="9pm the night before", 
        value=data_date_time_tomorrow
    )
    data_model.append(data_date_time_9pm)
    data_content = Content(text="put out Quinten's boots by the front door")
    data_model.append(data_content)
    
    # start code block to test
    # end code block to test
    
    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 0
