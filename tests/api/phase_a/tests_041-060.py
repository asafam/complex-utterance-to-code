from entities.generic import *
from entities.clock import *
from entities.calendar import *
from entities.home import *
from entities.message import *
from entities.music import *
from entities.navigation import *
from entities.reminder import *
from entities.shopping import *
from entities.weather import *
from actions.calendar import Calendar
from actions.clock import Clock
from actions.calendar import Events
from actions.home import Home
from actions.messages import Messages
from actions.music import Music
from actions.navigation import Navigation
from actions.reminders import Reminders
from actions.responder import Responder
from actions.shopping import Shopping
from actions.weather import Weather
from providers.data_model import DataModel
from datetime import datetime, timedelta
from tests.test_utils import *
import utils


def test_52():
    """
    Set a reminder at 3:00 PM that I will need to pick up my items from the store, and text Jason to meet me at the store at 2:50 PM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(
        text="at 3 PM", value=datetime.now.replace(hour=15, minute=0)
    )
    data_model.append(data_date_time)
    data_content = Content(
        text="I will need to pick up my items from the store",
        value="I will need to pick up my items from the store",
    )
    data_model.append(data_content)
    data_recipient = Contact(text="Jason", value="Jason Smith")
    data_model.append(data_recipient)
    data_content_message = Content(
        text="meet me at the store at 2:50 PM", value="meet me at the store at 2:50 PM"
    )
    data_model.append(data_content_message)

    # code block to test

    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert data_reminder.data.get("date_time") == data_date_time
    assert data_reminder.data.get("content") == data_content

    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert data_message.data.get("recipient") == data_recipient
    assert data_message.data.get("content") == data_content_message


def test_54():
    """
    Set the thermostat to 70 degrees and play my romantic playlist.
    """
    # test data
    data_model = DataModel(reset=True)
    data_home_device_action = HomeDeviceAction(text="set")
    data_model.append(data_home_device_action)
    data_home_device_name = HomeDeviceName(text="the thermostat", value="thermostat")
    data_model.append(data_home_device_name)
    data_home_device_value = HomeDeviceValue(text="70 degrees", value=70)
    data_model.append(data_home_device_value)
    data_playlist = Playlist(text="my romantic playlist", value="my romantic playlist")
    data_model.append(data_playlist)

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

    data_musics = data_model.get_data(MusicEntity)
    assert len(data_musics) == 1
    data_music = data_musics[0]
    assert test_equal(data_music.data.get("playlist"), data_playlist)


def test_55():
    """
    Remind me to send an email to Mom and Dad tomorrow and delete the appointment in my calendar for Tuesday.
    """
    # test data
    data_model = DataModel(reset=True)
    data_content = Content(
        text="send an email to Mom and Dad", value="send an email to Mom and Dad"
    )
    data_model.append(data_content)
    data_date_time_tomorrow = DateTime(
        text="tomorrow",
        value=datetime.now() + timedelta(days=1),
    )
    data_model.append(data_date_time_tomorrow)
    data_date_time = DateTime(
        text="Tuesday",
        value=datetime.now() + timedelta(days=((7 + 2 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time)
    data_calendar = EventCalendar(text="my calendar", value="my calendar")
    data_model.append(data_calendar)
    data_model.append(EventEntity(date_time=data_date_time))

    # start code block to test
    # end code block to test

    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert data_reminder.data.get("date_time") == data_date_time_tomorrow
    assert data_reminder.data.get("content") == data_content

    data_events = data_model.get_data(EventEntity)
    assert len(data_events) == 0


def test_58_a():
    """
    If Walmart has Jurassic World on bluray, buy it so I can pick it up tomorrow morning.
    """
    # test data
    data_model = DataModel(reset=True)
    data_store = Location(text="Walmart", value="Walmart")
    data_model.append(data_store)
    data_product = Product(
        text="Jurassic World on bluray", value="Jurassic World on bluray"
    )
    data_model.append(data_product)
    data_model.append(ProductEntity(location=data_store, product=data_product))

    # start code block to test
    # end code block to test

    # assertions
    data_orders = data_model.get_data(OrderEntity)
    assert len(data_orders) == 1
    data_order = data_orders[0]
    assert data_order.data.get("location") == data_store
    assert data_order.data.get("product") == data_product


def test_58_b():
    """
    If Walmart has Jurassic World on bluray, buy it so I can pick it up tomorrow morning.
    """
    # test data
    data_model = DataModel(reset=True)
    data_store = Location(text="Walmart", value="Walmart")
    data_model.append(data_store)
    data_product = Product(
        text="Jurassic World on bluray", value="Jurassic World on bluray"
    )
    data_model.append(data_product)

    # start code block to test
    # end code block to test

    # assertions
    data_orders = data_model.get_data(OrderEntity)
    assert len(data_orders) == 0


def test_59():
    """
    Get directions to Portland, and tell me if it will snow along the route in the next hour
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination = Location(text="Portland", value="Portland")
    data_model.append(data_destination)
    data_direction = NavigationDirectionEntity(destination=data_destination)
    data_model.append(data_direction)
    data_weather_attribute = WeatherAttribute(text="snow", value="snow")
    data_model.append(data_weather_attribute)
    data_location = Location(text="along the route", value=data_direction)
    data_model.append(data_location)
    data_date_time = DateTime(
        text="in the next hour",
        value=datetime.now() + timedelta(hours=1),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            location=data_location,
            weather_attribute=data_weather_attribute,
            date_time=data_date_time,
        )
    )

    # start code block to test
    # end code block to test

    # assertions
    data_navigation_directions = data_model.get_data(NavigationDirectionEntity)
    assert len(data_navigation_directions) == 1
    data_navigation_direction = data_navigation_directions[0]
    assert data_navigation_direction.data.get("destination") == data_destination

    data_weather_forecasts_list = data_model.get_data(WeatherForecastEntity)
    assert len(data_weather_forecasts_list) == 1
    data_weather_forecasts = data_weather_forecasts_list[0]
    assert (
        data_weather_forecasts[0].data.get("weather_attribute")
        == data_weather_attribute
    )
    assert data_weather_forecasts[0].data.get("location") == data_location
    assert data_weather_forecasts[0].data.get("date_time") == data_date_time


def test_60_a():
    """
    Check the weather and text Mike that I will meet them later if it's hot.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="hot", value="hot")
    data_model.append(data_weather_attribute)
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute))
    data_recipient = Contact(text="Mike", value="Mike Miller")
    data_model.append(data_recipient)
    data_content = Content(
        text="I will meet them later", value="I will meet them later"
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert data_message.data.get("recipient") == data_recipient
    assert data_message.data.get("content") == data_content


def test_60_b():
    """
    Check the weather and text Mike that I will meet them later if it's hot.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="cold", value="cold")
    data_model.append(data_weather_attribute)
    data_model.append(WeatherForecastEntity(weather_attribute=data_weather_attribute))
    data_recipient = Contact(text="Mike", value="Mike Miller")
    data_model.append(data_recipient)
    data_content = Content(
        text="I will meet them later", value="I will meet them later"
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 0


def test_63_a():
    """
    If the weather is going to be sunny Saturday morning, send an email to Ashley asking if she wants to go for a hike.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute)
    data_date_time_sat = DateTime(
        text="Saturday morning",
        value=datetime.now() + timedelta(days=((7 + 5 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_sat)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time_sat
        )
    )

    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Ashley", value="Ashley Smith")
    data_model.append(data_recipient)
    data_content = Content(text="she wants to go for a hike")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert test_equal(
        data_message.data.get("message_content_type"), data_message_content_type
    )
    assert test_equal(data_message.data.get("recipient"), data_recipient)
    assert test_equal(data_message.data.get("content"), data_content)


def test_63_b():
    """
    If the weather is going to be sunny Saturday morning, send an email to Ashley asking if she wants to go for a hike.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="rainy")
    data_model.append(data_weather_attribute)
    data_date_time_sat = DateTime(
        text="Saturday morning",
        value=datetime.now() + timedelta(days=((7 + 5 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_sat)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time_sat
        )
    )

    data_message_content_type = MessageContentType(text="email")
    data_model.append(data_message_content_type)
    data_recipient = Contact(text="Ashley", value="Ashley Smith")
    data_model.append(data_recipient)
    data_content = Content(text="she wants to go for a hike")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 0


def test_65():
    """
    Send a message to my friends list on Monday telling them to remember to vote and set a reminder to me to remember to vote.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipients = []
    for friend in ["Tom", "Jerry", "Mike", "Ashley"]:
        data_recipient = Contact(text=friend)
        data_model.append(data_recipient)
        data_recipients.append(data_recipient)
    data_date_time_mon = DateTime(
        text="Monday",
        value=datetime.now() + timedelta(days=((7 + 0 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_mon)
    data_content = Content(text="remember to vote")
    data_model.append(data_content)
    data_message_content_type = MessageContentType(text="message")
    data_model.append(data_message_content_type)

    # start code block to test
    # end code block to test

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 4
    for data_recipient in data_recipients:
        assert filter(
            lambda data_message: test_equal(
                data_message.data.get("recipient"), data_recipient
            )
            and test_equal(data_message.data.get("content"), data_content)
            and test_equal(data_message.data.get("date_time"), data_date_time_mon),
            data_messages,
        )


def test_66():
    """
    Show me all of the musical events within 10 miles of me.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_type = EventType(text="musical")
    data_model.append(data_event_type)
    data_location = Location(text="within 10 miles of me")
    data_model.append(data_location)
    for i in range(3):
        data_event_name = EventName(text="event {}".format(i))
        data_model.append(
            EventEntity(
                event_name=data_event_name,
                event_type=data_event_type,
                location=data_location,
            )
        )

    # start code block to test
    # end code block to test

    # assertions
    data_events = data_model.get_data(EventEntity)
    assert len(data_events) == 3
    for _ in range(3):
        assert filter(
            lambda data_message: test_equal(
                data_message.data.get("event_type"), data_event_type
            )
            and test_equal(data_message.data.get("location"), data_location),
            data_events,
        )


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
    # end code block to test

    # assertions
    data_musics = data_model.get_data(MusicEntity)
    assert len(data_musics) == 1
    data_music = data_musics[0]
    assert test_equal(data_music.data.get("playlist"), data_playlist)

    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert test_equal(data_message.data.get("recipient"), data_recipient)
    assert test_equal(data_message.data.get("content"), data_content)


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
    data_event_type = EventType("game")
    data_model.append(data_event_type)
    data_date_time_5pm = DateTime(text="5 PM", value=datetime.now().replace(hour=17))
    data_model.append(data_date_time_5pm)
    data_model.append(NavigationTrafficInfoEntity(date_time=data_date_time_5pm))

    # start code block to test
    # end code block to test

    # assertions
    data_event_tickets = data_model.get_data(EventTicketEntity)
    assert len(data_event_tickets) == 1
    data_event_ticket = data_event_tickets[0]
    assert test_not_none(len(data_event_ticket.data.get("events")))
    assert test_equal(len(data_event_ticket.data.get("events")), 1)
    assert test_equal(
        data_event_ticket.data.get("events")[0].data.get("date_time"),
        data_date_time_tomorrow,
    )
    assert test_equal(
        data_event_ticket.data.get("events")[0].data.get("event_name"), data_event_name
    )
    assert test_equal(
        data_event_ticket.data.get("events")[0].data.get("event_type"), data_event_type
    )

    data_nav_traffic_infos_list = data_model.get_data(NavigationTrafficInfoEntity)
    assert len(data_nav_traffic_infos_list) == 1
    data_nav_traffic_infos = data_nav_traffic_infos_list[0]
    assert test_equal(data_nav_traffic_infos.data.get("date_time"), data_date_time_5pm)


def test_71():
    """
    Set timer to 30 mins and remind me to take the fish out of the oven.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(
        text="30 mins", value=datetime.now() + timedelta(minutes=30)
    )
    data_model.append(data_date_time)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_content = Content(text="take the fish out of the oven")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_timers = data_model.get_data(TimerEntity)
    assert len(data_timers) == 1
    data_timer = data_timers[0]
    assert test_equal(data_timer.data.get("date_time"), data_date_time)

    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert test_equal(data_reminder.data.get("person_reminded"), data_person_reminded)
    assert test_equal(data_reminder.data.get("content"), data_content)


def test_72_a():
    """
    Check the weather and if it's above 80 degrees, set a reminder on my calendar for "Go to the park later"
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_temperature = WeatherTemperature(text="above 80 degrees")
    data_model.append(data_weather_temperature)
    data_model.append(
        WeatherForecastEntity(weather_temperature=data_weather_temperature)
    )
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_content = Content(text="Go to the park later")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert test_equal(len(data_reminder.data.get("calendar")), data_calendar)
    assert test_equal(len(data_reminder.data.get("content")), data_content)


def test_72_b():
    """
    Check the weather and if it's above 80 degrees, set a reminder on my calendar for "Go to the park later"
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_temperature = WeatherTemperature(text="above 80 degrees")
    data_model.append(data_weather_temperature)
    data_weather_temperature_neg = WeatherTemperature(text="less than 80 degrees")
    data_model.append(
        WeatherForecastEntity(weather_temperature=data_weather_temperature_neg)
    )
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_content = Content(text="Go to the park later")
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    data_reminders = data_model.get_data(ReminderEntity)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert test_equal(len(data_reminder.data.get("calendar")), data_calendar)
    assert test_equal(len(data_reminder.data.get("content")), data_content)


def test_73():
    """
    Remind me on Sunday about my doctor's appointment next Monday and give me directions to the doctor's office.
    """
    # test data
    data_model = DataModel(reset=True)
    data_person_reminded = Contact(text="me")
    data_model.append(data_person_reminded)
    data_date_time_sunday = DateTime(
        text="Sunday",
        value=datetime.now() + timedelta(days=((7 + 6 - datetime.now().weekday()) % 7)),
    )
    data_model.append(data_date_time_sunday)
    data_content = Content(text="my doctor's appointment next Monday")
    data_model.append(data_content)
    data_destination = Location(text="doctor's office")
    data_model.append(data_destination)
    data_model.append(NavigationDirectionEntity(destination=data_destination))

    # start code block to test
    # end code block to test

    # assertions
    data_reminders = data_model.get_data(Reminders)
    assert len(data_reminders) == 1
    data_reminder = data_reminders[0]
    assert test_equal(
        len(data_reminder.data.get("person_reminded")), data_person_reminded
    )
    assert test_equal(len(data_reminder.data.get("date_time")), data_date_time_sunday)
    assert test_equal(len(data_reminder.data.get("content")), data_content)

    data_navigation_directions_list = data_model.get_data(NavigationDirectionEntity)
    assert len(data_navigation_directions_list) == 1
    data_navigation_directions = data_navigation_directions_list[0]
    assert len(data_navigation_directions) == 1
    assert test_equal(
        data_navigation_directions[0].data.get("destination"), data_destination
    )


def test_75():
    """
    For Shakey Graves' upcoming summer tour, what will be the closest show to me and how many miles away is the venue?
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="Shakey Graves' upcoming summer tour")
    data_model.append(data_event_name)
    data_model.append(EventEntity(event_name=data_event_name, closest=10))
    for i in range(3):
        data_entity = EventEntity(event_name=data_event_name)
        data_model.append(data_entity)
        data_location = Location(value=data_entity)
        data_model.append(data_location)
        data_model.append(
            NavigationDistanceEntity(destination=data_location, closest=10 + i)
        )

    # start code block to test
    event_name = EventName.resolve_from_text("Shakey Graves' upcoming summer tour")
    events = Events.find_events(event_name=event_name)
    nav_distances = []
    for event in events:
        destination = Location.resolve_from_entity(event)
        nav_distances += Navigation.find_distance(destination=destination)
    closest_event = utils.first(utils.sort(nav_distances, "closet"))
    Responder.respond(response=closest_event)
    # end code block to test

    # assertions
    navigation_distances = data_model.get_data(NavigationDistanceEntity)
    assert len(navigation_distances) == 1
    navigation_distance = navigation_distances[0]
    assert test_not_none(
        navigation_distance.data.get("destination")
        and navigation_distance.data.get("destination").data.get("entity")
    )
    assert test_equal(
        navigation_distance.data.get("destination")
        .data.get("entity")
        .data.get("event_name"),
        data_event_name,
    )


def test_76_a():
    """
    If is is raining at 8pm turn the heat up 5 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(
        text="8pm",
        value=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time
        )
    )
    data_home_device_name = HomeDeviceName(text="heat")
    data_model.append(data_home_device_name)
    data_home_device_action = HomeDeviceAction(text="turn the heat up")
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="5 degrees")
    data_model.append(data_home_device_value)

    # start code block to test
    # end code block to test

    # assertions
    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert len(data_home_devices) == 1
    data_home_device = data_home_devices[0]
    assert test_equal(
        len(data_home_device.data.get("device_name")), data_home_device_name
    )
    assert test_equal(
        len(data_home_device.data.get("device_action")), data_home_device_action
    )
    assert test_equal(
        len(data_home_device.data.get("device_value")), data_home_device_value
    )


def test_76_b():
    """
    If is is raining at 8pm turn the heat up 5 degrees.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="raining")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="not raining")
    data_date_time = DateTime(
        text="8pm",
        value=datetime.now().replace(hour=20, minute=0, second=0, microsecond=0),
    )
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg, date_time=data_date_time
        )
    )
    data_home_device_name = HomeDeviceName(text="heat")
    data_model.append(data_home_device_name)
    data_home_device_action = HomeDeviceAction(text="turn the heat up")
    data_model.append(data_home_device_action)
    data_home_device_value = HomeDeviceValue(text="5 degrees")
    data_model.append(data_home_device_value)

    # start code block to test
    # end code block to test

    # assertions
    data_home_devices = data_model.get_data(HomeDeviceEntity)
    assert len(data_home_devices) == 0
