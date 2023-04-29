from entities.generic import *
from entities.events import *
from entities.message import *
from entities.music import *
from entities.navigation import *
from entities.reminder import *
from entities.shopping import *
from entities.weather import *
from actions.calendar import Calendar
from actions.clock import *
from actions.events import *
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
from test_utils import assert_equal, assert_not_none, assert_test, test_equal


def test_0():
    """
    Check the availability of Pepsi at Walmart and also check it at Walgreens.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_pepsi = Product(text="Pepsi")
    data_model.append(data_product_pepsi)
    data_product_coca = Product(text="coca cola")
    data_model.append(data_product_coca)
    data_location1 = DateTime(text="Walmart")
    data_model.append(data_location1)
    data_location2 = DateTime(text="Walgreens")
    data_model.append(data_location2)
    data_model.append(
        ProductEntity(product=data_product_pepsi, location=data_location1)
    )
    data_model.append(
        ProductEntity(product=data_product_pepsi, location=data_location2)
    )
    data_model.append(ProductEntity(product=data_product_coca, location=data_location1))
    data_model.append(ProductEntity(product=data_product_coca, location=data_location2))

    # start code block to test
    results = []

    product = Product.resolve_from_text("Pepsi")
    location = DateTime.resolve_from_text("Walmart")
    products = Shopping.find_products(product=product, location=location)
    results += products

    location = DateTime.resolve_from_text("Walgreens")
    products = Shopping.find_products(product=product, location=location)
    results += products

    Responder.respond(response=results)
    # end code block to test

    # assertions
    test_results = {}
    data_products_list = data_model.get_response([ProductEntity])
    assert_equal(len(data_products_list), 1, test_results)
    data_products = data_products_list[0]
    assert_equal(len(data_products), 2, test_results)
    assert_equal(data_products[0].data.get("product"), data_product_pepsi, test_results)
    assert_equal(data_products[0].data.get("location"), data_location1, test_results)
    assert_equal(data_products[1].data.get("product"), data_product_pepsi, test_results)
    assert_equal(data_products[1].data.get("location"), data_location2, test_results)
    assert_test(test_results)


def test_1_a():
    """
    If it's raining tomorrow morning, set my alarm for 7:30, if it's not, set my alarm for 8.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(
        text="tomorrow morning", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="raining", value="rain")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time
        )
    )
    data_date_time730 = DateTime(text="7:30", value=datetime(2022, 11, 13, 7, 30))
    data_model.append(data_date_time730)
    data_date_time800 = DateTime(text="8", value=datetime(2022, 11, 13, 8, 00))
    data_model.append(data_date_time800)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow morning")
    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        date_time = DateTime.resolve_from_text("7:30")
        alarm = Alarm.create_alarm(date_time=date_time)
    else:
        date_time = DateTime.resolve_from_text("8")
        alarm = Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}
    data_alarms_list = data_model.get_data(AlarmEntity)
    assert_equal(len(data_alarms_list), 1, test_results)
    data_alarm = data_alarms_list[0]
    assert_equal(data_alarm.data.get("date_time"), data_date_time730, test_results)
    assert_test(test_results)


def test_1_b():
    """
    If it's raining tomorrow morning, set my alarm for 7:30, if it's not, set my alarm for 8.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(
        text="tomorrow morning", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="raining", value="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny", value="sun")
    data_model.append(data_weather_attribute_neg)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg, date_time=data_date_time
        )
    )
    data_date_time730 = DateTime(text="7:30", value=datetime(2022, 11, 13, 7, 30))
    data_model.append(data_date_time730)
    data_date_time800 = DateTime(text="8", value=datetime(2022, 11, 13, 8, 00))
    data_model.append(data_date_time800)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow morning")
    weather_attribute = WeatherAttribute.resolve_from_text("raining")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        date_time = DateTime.resolve_from_text("7:30")
        alarm = Alarm.create_alarm(date_time=date_time)
    else:
        date_time = DateTime.resolve_from_text("8")
        alarm = Alarm.create_alarm(date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}
    data_alarms_list = data_model.get_data(AlarmEntity)
    assert_equal(len(data_alarms_list), 1, test_results)
    data_alarm = data_alarms_list[0]
    assert_equal(data_alarm.data.get("date_time"), data_date_time800, test_results)
    assert_test(test_results)


def test_2():
    """
    Play the new Taylor Swift album and pull up my shopping list for today.
    """
    # test data
    data_model = DataModel(reset=True)
    data_artist = Artist(text="Taylor Swift", value="Taylor Swift")
    data_model.append(data_artist)
    data_music_type = MusicType(text="album", value="album")
    data_model.append(data_music_type)
    data_model.append(MusicEntity(artist=data_artist, music_type=data_music_type))
    data_date_time_today = DateTime(text="today", value=datetime.now())
    data_model.append(data_date_time_today)
    data_model.append(ShoppingListEntity(date_time=data_date_time_today))
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_model.append(ShoppingListEntity(date_time=data_date_time_tomorrow))

    # start code block to test
    artist = Artist.resolve_from_text("Taylor Swift")
    music_type = MusicType.resolve_from_text("album")
    Music.play_music(artist=artist, music_type=music_type)

    date_time = DateTime.resolve_from_text("today")
    shopping_lists = Shopping.find_shopping_lists(date_time=date_time)
    Responder.respond(response=shopping_lists)
    # end code block to test

    # assertions
    test_results = {}
    data_music_list = data_model.get_data(MusicEntity)
    assert_equal(len(data_music_list), 1, test_results)
    data_music = data_music_list[0]
    assert_equal(data_music.data.get("artist"), data_artist, test_results)
    assert_equal(data_music.data.get("music_type"), data_music_type, test_results)

    data_shopping_lists_list = data_model.get_response([ShoppingListEntity])
    assert_equal(len(data_shopping_lists_list), 1, test_results)
    data_shopping_list = data_shopping_lists_list[0]
    assert_equal(
        data_shopping_list[0].data.get("date_time"), data_date_time_today, test_results
    )
    assert_test(test_results)


def test_3_a():
    """
    Send a message to dad if it rains tomorrow.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="dad", value="Father")
    data_model.append(data_recipient)
    data_date_time = DateTime(text="tomorrow", value=datetime.now() + timedelta(days=1))
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="rains", value="rain")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute, date_time=data_date_time
        )
    )

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_attribute = WeatherAttribute.resolve_from_text("rains")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        recipient = Contact.resolve_from_text("dad")
        message = Messages.send_message(recipient=recipient)
    # end code block to test

    # assertions
    test_results = {}
    data_message_list = data_model.get_data(MessageEntity)
    assert_equal(len(data_message_list), 1, test_results)
    data_message = data_message_list[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_test(test_results)


def test_3_b():
    """
    Send a message to dad if it rains tomorrow.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="dad", value="Father")
    data_model.append(data_recipient)
    data_date_time = DateTime(text="tomorrow", value=datetime.now() + timedelta(days=1))
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="rains", value="rain")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="sunny", value="sun")
    data_model.append(data_weather_attribute_neg)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg, date_time=data_date_time
        )
    )

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_attribute = WeatherAttribute.resolve_from_text("rains")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        recipient = Contact.resolve_from_text("dad")
        message = Messages.send_message(recipient=recipient)
    # end code block to test

    # assertions
    test_results = {}
    data_message_list = data_model.get_data(MessageEntity)
    assert_equal(len(data_message_list), 0, test_results)
    assert_test(test_results)


def test_4():
    """
    Give me directions to Navy pier in Chicago and tell me what the current traffic is looking like.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="Navy pier in Chicago", value="Navy pier in Chicago")
    data_model.append(data_location)
    data_model.append(NavigationDirectionEntity(destination=data_location))
    data_model.append(NavigationTrafficInfoEntity(destination=data_location))

    # start code block to test
    destination = Location.resolve_from_text("Navy pier in Chicago")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)
    traffic_info = Navigation.find_traffic_info(destination=destination)
    Responder.respond(response=traffic_info)
    # end code block to test

    # assertions
    test_results = {}
    data_navigation_directions_list = data_model.get_response(
        [NavigationDirectionEntity]
    )
    assert_equal(len(data_navigation_directions_list), 1, test_results)
    data_navigation_directions = data_navigation_directions_list[0]
    assert_equal(
        data_navigation_directions[0].data.get("destination"),
        data_location,
        test_results,
    )

    data_navigation_traffic_info_list = data_model.get_response(
        [NavigationTrafficInfoEntity]
    )
    assert_equal(len(data_navigation_traffic_info_list), 1, test_results)
    data_navigation_traffic_info = data_navigation_traffic_info_list[0]
    assert_equal(
        data_navigation_traffic_info[0].data.get("destination"),
        data_location,
        test_results,
    )
    assert_test(test_results)


def test_5():
    """
    Check the next time Blink 182 will be in Chicago and tell me the ticket prices.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="Blink 182", value="Blink 182 Tour")
    data_model.append(data_event_name)
    data_location = Location(text="Chicago", value="Chicago")
    data_model.append(data_location)
    data_event = EventEntity(event_name=data_event_name, location=data_location)
    data_model.append(data_event)
    data_model.append(EventTicketEntity(event=data_event))

    # start code block to test
    event_name = EventName.resolve_from_text("Blink 182")
    location = Location.resolve_from_text("Chicago")
    events = Events.find_events(event_name=event_name, location=location)
    Responder.respond(response=events)

    tickets = Events.find_events_tickets(events=events)
    Responder.respond(response=tickets)
    # end code block to test

    # assertions
    test_results = {}
    data_events_list = data_model.get_response([EventEntity])
    assert_equal(len(data_events_list), 1, test_results)
    data_events = data_events_list[0]
    assert_equal(data_events[0].data.get("event_name"), data_event_name, test_results)
    assert_equal(data_events[0].data.get("location"), data_location, test_results)
    data_tickets_list = data_model.get_response([EventTicketEntity])
    assert_equal(len(data_tickets_list), 1, test_results)
    data_tickets = data_tickets_list[0]
    assert_equal(data_tickets[0].data.get("event"), data_event, test_results)
    assert_test(test_results)


def test_6():
    """
    Remind me tomorrow to email Jim about lunch and schedule a reservation for noon at the cafe.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime(2022, 11, 14, 00, 00)
    )
    data_model.append(data_date_time_tomorrow)
    data_contact = Contact(text="me", value="Asaf")
    data_model.append(data_contact)
    data_content = Content(text="email Jim about lunch", value="email Jim about lunch")
    data_model.append(data_content)
    data_date_time_noon = DateTime(text="noon", value=datetime(2022, 11, 13, 12, 00))
    data_model.append(data_date_time_noon)
    data_location = Location(text="the cafe", value="the cafe")
    data_model.append(data_location)

    # start code block to test
    date_time = DateTime.resolve_from_text("tomorrow")
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("email Jim about lunch")
    Reminders.create_reminder(
        date_time=date_time, content=content, person_reminded=person_reminded
    )
    date_time = DateTime.resolve_from_text("noon")
    location = Location.resolve_from_text("the cafe")
    Events.schedule_event(date_time=date_time, location=location)
    # end code block to test

    # assertions
    test_results = {}
    data_reminders_list = data_model.get_data(ReminderEntity)
    assert_equal(len(data_reminders_list), 1, test_results)
    data_reminders = data_reminders_list[0]
    assert_equal(
        data_reminders.data.get("date_time"), data_date_time_tomorrow, test_results
    )
    assert_equal(data_reminders.data.get("person_reminded"), data_contact, test_results)

    data_events_list = data_model.get_data(EventEntity)
    assert_equal(len(data_events_list), 1, test_results)
    data_events = data_events_list[0]
    assert_equal(data_events.data.get("date_time"), data_date_time_noon, test_results)
    assert_equal(data_events.data.get("location"), data_location, test_results)
    assert_test(test_results)


def test_7():
    """
    Can you place an order for two turkeys to arrive the 22nd, and remind me about it on the 21st?
    """
    # test data
    data_model = DataModel(reset=True)
    data_product = Product(text="two turkeys", value="two turkeys")
    data_model.append(data_product)
    data_date_time_22 = DateTime(text="22nd", value=datetime(2022, 11, 22))
    data_model.append(data_date_time_22)
    data_contact = Contact(text="me", value="me")
    data_model.append(data_contact)
    data_date_time_21 = DateTime(text="21st", value=datetime(2022, 11, 21))
    data_model.append(data_date_time_21)

    # start code block to test
    product = Product.resolve_from_text("two turkeys")
    date_time = DateTime.resolve_from_text("22nd")
    order = Shopping.create_order(products=product, date_time=date_time)
    date_time = DateTime.resolve_from_text("21st")
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_entity(order)
    Reminders.create_reminder(
        date_time=date_time, person_reminded=person_reminded, content=content
    )
    # end code block to test

    # assertions
    test_results = {}
    data_orders_list = data_model.get_data(OrderEntity)
    assert_equal(len(data_orders_list), 1, test_results)
    data_orders = data_orders_list[0]
    assert_equal(data_orders.data.get("date_time"), data_date_time_22, test_results)
    assert_equal(data_orders.data.get("products"), data_product, test_results)

    data_reminder_list = data_model.get_data(ReminderEntity)
    assert_equal(len(data_reminder_list), 1, test_results)
    data_reminder = data_reminder_list[0]
    assert_equal(data_reminder.data.get("date_time"), data_date_time_21, test_results)
    assert_equal(data_reminder.data.get("person_reminded"), data_contact, test_results)
    assert_not_none(data_reminder.data.get("content"), test_results)
    assert_equal(
        data_reminder.data.get("content").data.get("value"), data_orders, test_results
    )
    assert_test(test_results)


def test_8():
    """
    How long will it take to get to AMC theater at 8pm tonight and tell me what tonight's weather outlook is.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="AMC theater", value="AMC theater")
    data_model.append(data_location)
    data_date_time_8pm = DateTime(
        text="at 8pm tonight", value=datetime(2022, 11, 13, 20, 00)
    )
    data_model.append(data_date_time_8pm)
    data_model.append(
        NavigationEstimatedArrivalEntity(
            destination=data_location, arrival_date_time=data_date_time_8pm
        )
    )
    data_date_time_tonight = DateTime(
        text="tonight", value=datetime(2022, 11, 13, 18, 00)
    )
    data_model.append(data_date_time_tonight)
    data_model.append(WeatherForecastEntity(date_time=data_date_time_tonight))

    # start code block to test
    destination = Location.resolve_from_text("AMC theater")
    arrival_date_time = DateTime.resolve_from_text("at 8pm tonight")
    navigation_arrival = Navigation.find_estimated_arrival(
        destination=destination, arrival_date_time=arrival_date_time
    )
    Responder.respond(response=navigation_arrival)

    date_time = DateTime.resolve_from_text("tonight")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time,
    )
    Responder.respond(response=weather_forecasts)
    # end code block to test

    # assertions
    test_results = {}
    data_estimated_arrivals_list = data_model.get_response(
        [NavigationEstimatedArrivalEntity]
    )
    assert_equal(len(data_estimated_arrivals_list), 1, test_results)
    data_estimated_arrivals = data_estimated_arrivals_list[0]
    assert_equal(
        data_estimated_arrivals[0].data.get("destination"), data_location, test_results
    )
    assert_equal(
        (
            data_estimated_arrivals[0].data.get("arrival_date_time"),
            data_date_time_8pm,
            test_results,
        )
    )

    data_weather_forecasts_list = data_model.get_response([WeatherForecastEntity])
    assert_equal(len(data_weather_forecasts_list), 1, test_results)
    data_weather_forecasts = data_weather_forecasts_list[0]
    assert_equal(
        data_weather_forecasts[0].data.get("date_time"),
        data_date_time_tonight,
        test_results,
    )
    assert_test(test_results)


def test_9():
    """
    Check the weather for the 4th of July and send a text to Grandpa to invite him over and tell him the weather.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="the 4th of July", value=datetime(2022, 7, 4))
    data_model.append(data_date_time)
    data_weather_forecasts = WeatherForecastEntity(date_time=data_date_time)
    data_model.append(data_weather_forecasts)
    data_contact = Contact(text="Grandpa", value="Grandpa")
    data_model.append(data_contact)
    data_content1 = Content(text="invite him over", value="invite him over")
    data_model.append(data_content1)
    data_content2 = Content(text="tell him the weather", value=data_weather_forecasts)
    data_model.append(data_content2)

    # start code block to test
    date_time = DateTime.resolve_from_text("the 4th of July")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time,
    )
    Responder.respond(response=weather_forecasts)

    recipient = Contact.resolve_from_text("Grandpa")
    content = Content.resolve_from_text("invite him over")
    message = Messages.send_message(recipient=recipient, content=content)
    content = Content.resolve_from_entity(weather_forecasts)
    message = Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}
    data_weather_forecasts_list = data_model.get_response([WeatherForecastEntity])
    assert_equal(len(data_weather_forecasts_list), 1, test_results)
    data_weather_forecasts = data_weather_forecasts_list[0]
    assert_equal(
        data_weather_forecasts[0].data.get("date_time"), data_date_time, test_results
    )

    data_message_list = data_model.get_data(MessageEntity)
    assert_equal(len(data_message_list), 2, test_results)
    data_message = data_message_list[0]
    assert_equal(data_message.data.get("recipient"), data_contact, test_results)
    assert_equal(data_message.data.get("content"), data_content1, test_results)
    data_message = data_message_list[1]
    assert_equal(data_message.data.get("recipient"), data_contact, test_results)
    assert_equal(
        data_message.data.get("content").data.get("value"),
        data_weather_forecasts,
        test_results,
    )
    assert_test(test_results)


def test_10():
    """
    Set a timer for one hour and text Stacy that dinner will be ready in one hour.
    """
    # test data
    data_model = DataModel(reset=True)
    data_duration = DateTime(text="one hour", value=datetime(2022, 11, 14, 1, 0))
    data_model.append(data_duration)
    data_contact = Contact(text="Stacy", value="Stacy")
    data_model.append(data_contact)
    data_content = Content(text="dinner will be ready in one hour")
    data_model.append(data_content)

    # start code block to test
    duration = DateTime.resolve_from_text("one hour")
    Timer.create_timer(
        duration=duration,
    )

    recipient = Contact.resolve_from_text("Stacy")
    content = Content.resolve_from_text("dinner will be ready in one hour")
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}
    data_timer_list = data_model.get_data(TimerEntity)
    assert_equal(len(data_timer_list), 1, test_results)
    data_timer = data_timer_list[0]
    assert_equal(data_timer.data.get("duration"), data_duration, test_results)

    data_message_list = data_model.get_data(MessageEntity)
    assert_equal(len(data_message_list), 1, test_results)
    data_message = data_message_list[0]
    assert_equal(data_message.data.get("recipient"), data_contact, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_13_a():
    """
    If the weather is cold tomorrow please remind me to grab my winter jacket.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="cold", value="cold")
    data_model.append(data_weather_attribute)
    data_date_time = DateTime(text="tomorrow", value=datetime(2022, 11, 15))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time, weather_attribute=data_weather_attribute
        )
    )
    data_person_reminded = Contact(text="me", value="I")
    data_model.append(data_person_reminded)
    data_content = Content(
        text="grab my winter jacket.",
        value="grab my winter jacket.",
    )
    data_model.append(data_content)
    # end code block to test

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("cold")
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        person_reminded = Contact.resolve_from_text("me")
        content = Content.resolve_from_text("grab my winter jacket.")
        Reminders.create_reminder(
            person_reminded=person_reminded,
            content=content,
        )

    # assertions
    test_results = {}
    data_reminder_list = data_model.get_data(ReminderEntity)
    assert_equal(len(data_reminder_list), 1, test_results)
    data_reminder = data_reminder_list[0]
    assert_equal(
        data_reminder.data.get("person_reminded"), data_person_reminded, test_results
    )
    assert_equal(data_reminder.data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_13_b():
    """
    If the weather is cold tomorrow please remind me to grab my winter jacket.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="cold", value="cold")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="hot", value="hot")
    data_model.append(data_weather_attribute_neg)
    data_date_time = DateTime(text="tomorrow", value=datetime.now() + timedelta(days=1))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time, weather_attribute=data_weather_attribute_neg
        )
    )
    data_person_reminded = Contact(text="me", value="I")
    data_model.append(data_person_reminded)
    data_content = Content(
        text="grab my winter jacket.",
        value="grab my winter jacket.",
    )
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("cold")
    date_time = DateTime.resolve_from_text("tomorrow")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        person_reminded = Contact.resolve_from_text("me")
        content = Content.resolve_from_text("grab my winter jacket.")
        Reminders.create_reminder(
            person_reminded=person_reminded,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}
    data_reminder_list = data_model.get_data(ReminderEntity)
    assert_equal(len(data_reminder_list), 0, test_results)
    assert_test(test_results)


def test_14():
    """
    What is the weather going to be at 5:00 PM today and navigate destination set to home after 5:00 PM.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="5:00 PM today", value=datetime(2022, 11, 14, 17, 0))
    data_model.append(data_date_time)
    data_weather_attribute = WeatherAttribute(text="cold", value="cold")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time, weather_attribute=data_weather_attribute
        )
    )
    data_destination = Location(text="home", value="23e 8th st, new york, ny")
    data_model.append(data_destination)
    data_departure_date_time = DateTime(
        text="after 5:00 PM", value=datetime(2022, 11, 14, 17, 1)
    )
    data_model.append(data_departure_date_time)
    data_model.append(
        NavigationDirectionEntity(
            destination=data_destination, departure_date_time=data_departure_date_time
        )
    )

    # start code block to test
    date_time = DateTime.resolve_from_text("5:00 PM today")
    weather_forecasts = Weather.find_weather_forecasts(date_time=date_time)
    Responder.respond(response=weather_forecasts)

    destination = Location.resolve_from_text("home")
    departure_date_time = DateTime.resolve_from_text("after 5:00 PM")
    navigation_directions = Navigation.find_directions(
        destination=destination,
        departure_date_time=departure_date_time,
    )
    Responder.respond(response=navigation_directions)
    # end code block to test

    # assertions
    test_results = {}
    data_weather_forecasts_list = data_model.get_response([WeatherForecastEntity])
    assert_equal(len(data_weather_forecasts_list), 1, test_results)
    data_weather_forecasts = data_weather_forecasts_list[0]
    assert_equal(
        data_weather_forecasts[0].data.get("date_time"), data_date_time, test_results
    )
    assert_equal(
        data_weather_forecasts[0].data.get("weather_attribute"),
        data_weather_attribute,
        test_results,
        test_results,
    )

    data_navigation_directions_list = data_model.get_response(
        [NavigationDirectionEntity]
    )
    assert_equal(len(data_navigation_directions_list), 1, test_results)
    data_navigation_directions = data_navigation_directions_list[0]
    assert_equal(
        data_navigation_directions[0].data.get("departure_date_time"),
        data_departure_date_time,
        test_results,
    )
    assert_equal(
        data_navigation_directions[0].data.get("destination"),
        data_destination,
        test_results,
    )
    assert_test(test_results)


def test_15_a():
    """
    If it's snowing in Boulder, Colorado by 6pm, text Lauren to tell her to let the dog inside.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="snowing", value="snow")
    data_model.append(data_weather_attribute)
    data_location = Location(text="Boulder, Colorado")
    data_model.append(data_location)
    data_date_time = DateTime(text="by 6pm", value=datetime(2022, 11, 15, 18, 00))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute,
            location=data_location,
            date_time=data_date_time,
        )
    )

    data_recipient = Contact(text="Lauren", value="Lauren Hill")
    data_model.append(data_recipient)
    data_content = Content(
        text="let the dog inside",
        value="let the dog inside",
    )
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("snowing")
    location = Location.resolve_from_text("Boulder, Colorado")
    date_time = DateTime.resolve_from_text("by 6pm")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, location=location, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        recipient = Contact.resolve_from_text("Lauren")
        content = Content.resolve_from_text("let the dog inside")
        Messages.send_message(
            recipient=recipient,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_15_b():
    """
    If it's snowing in Boulder, Colorado by 6pm, text Lauren to tell her to let the dog inside.
    """
    # test data
    data_model = DataModel(reset=True)
    data_weather_attribute = WeatherAttribute(text="snowing", value="snow")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="rain", value="rain")
    data_model.append(data_weather_attribute_neg)
    data_location = Location(text="Boulder, Colorado")
    data_model.append(data_location)
    data_date_time = DateTime(text="by 6pm", value=datetime(2022, 11, 15, 18, 00))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg,
            location=data_location,
            date_time=data_date_time,
        )
    )

    data_recipient = Contact(text="Lauren", value="Lauren Hill")
    data_model.append(data_recipient)
    data_content = Content(
        text="let the dog inside",
        value="let the dog inside",
    )
    data_model.append(data_content)

    # start code block to test
    weather_attribute = WeatherAttribute.resolve_from_text("snowing")
    location = Location.resolve_from_text("Boulder, Colorado")
    date_time = DateTime.resolve_from_text("by 6pm")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, location=location, weather_attribute=weather_attribute
    )
    expr = len(list(weather_forecasts)) > 0
    if expr:
        recipient = Contact.resolve_from_text("Lauren")
        content = Content.resolve_from_text("let the dog inside")
        Messages.send_message(
            recipient=recipient,
            content=content,
        )
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 0, test_results)
    assert_test(test_results)


def test_16():
    """
    Text my brother I am on my way and also tell me the current traffic conditions.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="my brother", value="Jim Hill")
    data_model.append(data_recipient)
    data_omw = Content(
        text="I am on my way",
        value="I am on my way",
    )
    data_model.append(data_omw)
    data_date_time = DateTime(text="current", value=datetime.now())
    data_model.append(data_date_time)
    data_model.append(NavigationTrafficInfoEntity(date_time=data_date_time))

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_omw, test_results)

    data_traffic_infos_list = data_model.get_data(NavigationTrafficInfoEntity)
    assert_equal(len(data_traffic_infos_list), 1, test_results)
    data_traffic_infos = data_traffic_infos_list[0]
    assert_equal(
        data_traffic_infos[0].data.get("date_time"), data_date_time, test_results
    )
    assert_test(test_results)


def test_17():
    """
    Start my shower playlist and text Lucas that I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out.
    """
    # test data
    data_model = DataModel(reset=True)
    data_playlist = Playlist(text="shower playlist")
    data_model.append(data_playlist)
    data_recipient = Contact(text="Lucas", value="Lucas Leonard")
    data_model.append(data_recipient)
    data_content = Content(
        text="I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out",
        value="I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out",
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_music_list = data_model.get_data(MusicEntity)
    assert_equal(len(data_music_list), 1, test_results)
    data_music = data_music_list[0]
    assert_equal(data_music.data.get("playlist"), data_playlist, test_results)

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_18():
    """
    Tell Abe to pick up bread on his way home and set a timer for 60 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="Abe", value="Abe Lincoln")
    data_model.append(data_recipient)
    data_content = Content(
        text="pick up bread on his way home",
        value="pick up bread on his way home",
    )
    data_model.append(data_content)
    data_duration = DateTime(
        text="60 minutes", value=datetime.now() + timedelta(minutes=60)
    )
    data_model.append(data_duration)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)

    data_music_list = data_model.get_data(TimerEntity)
    assert_equal(len(data_music_list), 1, test_results)
    data_music = data_music_list[0]
    assert_equal(data_music.data.get("duration"), data_duration, test_results)
    assert_test(test_results)


def test_19_a():
    """
    Check the weather in Indianapolis, and if it's sunny, text Bob to remind him about the concert today.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="Indianapolis", value="Indianapolis")
    data_model.append(data_location)
    data_weather_attribute = WeatherAttribute(text="sunny", value="sunny")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute,
            location=data_location,
        )
    )

    data_recipient = Contact(text="Bob", value="Robert Convington")
    data_model.append(data_recipient)
    data_content = Content(
        text="remind him about the concert today",
        value="remind him about the concert today",
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


def test_19_b():
    """
    Check the weather in Indianapolis, and if it's sunny, text Bob to remind him about the concert today.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="Indianapolis", value="Indianapolis")
    data_model.append(data_location)
    data_weather_attribute = WeatherAttribute(text="sunny", value="sunny")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="rain", value="rain")
    data_model.append(data_weather_attribute_neg)
    data_model.append(
        WeatherForecastEntity(
            weather_attribute=data_weather_attribute_neg,
            location=data_location,
        )
    )

    data_recipient = Contact(text="Bob", value="Robert Convington")
    data_model.append(data_recipient)
    data_content = Content(
        text="remind him about the concert today",
        value="remind him about the concert today",
    )
    data_model.append(data_content)

    # start code block to test
    # end code block to test

    # assertions
    test_results = {}
    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 0, test_results)
    assert_test(test_results)


def test_20():
    """
    Give me directions to the nearest movie theater and text Mike to meet me there in a half hour.
    """
    # test data
    data_model = DataModel(reset=True)
    data_destination1 = Location(
        text="movie theater", value="movie theater 1", nearest=100
    )
    data_model.append(data_destination1)
    data_destination2 = Location(
        text="movie theater", value="movie theater 2", nearest=1
    )
    data_model.append(data_destination2)
    data_destination3 = Location(
        text="movie theater", value="movie theater 3", nearest=30
    )
    data_model.append(data_destination3)
    data_model.append(
        NavigationDirectionEntity(
            destination=data_destination2,
        )
    )

    data_recipient = Contact(text="Mike", value="Michael Jordan")
    data_model.append(data_recipient)
    data_content = Content(
        text="meet me there in a half hour",
        value="meet me there in a half hour",
    )
    data_model.append(data_content)

    # start code block to test
    destinations = Location.resolve_from_text("movie theater")
    destinations = utils.sort(destinations, "nearest")
    destination = utils.first(destinations)
    navigation_directions = Navigation.find_directions(
        destination=destination,
    )
    Responder.respond(response=navigation_directions)
    # end code block to test

    recipient = Contact.resolve_from_text("Mike")
    content = Content.resolve_from_text("meet me there in a half hour")
    Messages.send_message(
        recipient=recipient,
        content=content,
    )

    # assertions
    test_results = {}
    data_navigation_directions_list = data_model.get_response(
        [NavigationDirectionEntity]
    )
    assert_equal(len(data_navigation_directions_list), 1, test_results)
    data_navigation_directions = data_navigation_directions_list[0]
    assert_equal(
        data_navigation_directions[0].data.get("destination"),
        data_destination2,
        test_results,
    )

    data_messages = data_model.get_data(MessageEntity)
    assert_equal(len(data_messages), 1, test_results)
    data_message = data_messages[0]
    assert_equal(data_message.data.get("recipient"), data_recipient, test_results)
    assert_equal(data_message.data.get("content"), data_content, test_results)
    assert_test(test_results)


def test_21():
    """
    Check my calendar for when my aunt's birthday is this month and then set a reminder for three days before, so I can remember to buy a gift.
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time = DateTime(text="this month", value=datetime(2022, 11, 8, 00, 00))
    data_model.append(data_date_time)
    data_date_time = DateTime(
        text="three days before", value=datetime(2022, 11, 5, 00, 00)
    )
    data_model.append(data_date_time)
    data_event_name = EventName(
        text="my aunt's birthday", value="Auntie Rachel's Birthday"
    )
    data_model.append(data_event_name)
    data_model.append(WeatherForecastEntity(date_time=data_date_time))
    data_content = Content(
        text="remember to buy a gift", value="remember to buy a gift"
    )
    data_model.append(data_content)

    # start code block to test
    event_name = EventName.resolve_from_text("my aunt's birthday")
    date_time = DateTime.resolve_from_text("this month")
    calendar_events = Calendar.find_calendar_events(
        event_name=event_name, date_time=date_time
    )
    calendar_event = utils.first(calendar_events)

    content = Content.resolve_from_text("go running")
    date_time = DateTime.resolve_from_entity(calendar_event, "three days before")
    Reminders.create_reminder(content=content, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}
    data_reminder_list = data_model.get_data(ReminderEntity)
    assert_equal(len(data_reminder_list), 1, test_results)
    data_reminder = data_reminder_list[0]
    assert_equal(data_reminder.data.get("content"), data_content, test_results)
    assert_equal(data_reminder.data.get("date_time"), data_date_time, test_results)
    assert_test(test_results)
