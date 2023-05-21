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


def test_0():
    """
    Check the availability of Pepsi at Walmart and also check it at Walgreens.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name_pepsi = ProductName(text="Pepsi")
    data_model.append(data_product_name_pepsi)
    data_product_name_coca = ProductName(text="coca cola")
    data_model.append(data_product_name_coca)
    data_location1 = Location(text="Walmart")
    data_model.append(data_location1)
    data_location2 = Location(text="Walgreens")
    data_model.append(data_location2)
    data_location3 = Location(text="CVS")
    data_model.append(data_location3)
    data_product1 = ProductEntity(
        product_name=data_product_name_pepsi, location=data_location1
    )
    data_model.append(data_product1)
    data_product2 = ProductEntity(
        product_name=data_product_name_pepsi, location=data_location2
    )
    data_model.append(data_product2)
    data_product3 = ProductEntity(
        product_name=data_product_name_coca, location=data_location1
    )
    data_model.append(data_product3)
    data_product4 = ProductEntity(
        product_name=data_product_name_coca, location=data_location2
    )
    data_model.append(data_product4)
    data_product5 = ProductEntity(
        product_name=data_product_name_pepsi, location=data_location3
    )
    data_model.append(data_product5)
    data_product6 = ProductEntity(
        product_name=data_product_name_pepsi, location=data_location1
    )
    data_model.append(data_product6)

    # start code block to test
    product_name = ProductName.resolve_from_text("Pepsi")
    location = Location.resolve_from_text("Walmart")
    products = Shopping.find_products(product_name=product_name, location=location)
    Responder.respond(response=products)

    location = Location.resolve_from_text("Walgreens")
    products = Shopping.find_products(product_name=product_name, location=location)
    Responder.respond(response=products)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([ProductEntity]))

    expected = [data_product1, data_product6]
    actual = next(iterator, None)
    response_assertions(expected, actual, test_results)

    expected = [data_product2]
    actual = next(iterator, None)
    response_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(AlarmEntity)
    expected = [{"date_time": data_date_time730}]
    entity_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(AlarmEntity)
    expected = [{"date_time": data_date_time800}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_2():
    """
    Play the new Taylor Swift album and pull up my shopping list for today.
    """
    # test data
    data_model = DataModel(reset=True)
    data_album = Album(text="the new Taylor Swift album")
    data_model.append(data_album)
    data_date_time_today = DateTime(text="today", value=datetime.now())
    data_model.append(data_date_time_today)
    data_shopping_list1 = ShoppingListEntity(date_time=data_date_time_today)
    data_model.append(data_shopping_list1)
    data_date_time_tomorrow = DateTime(
        text="tomorrow", value=datetime.now() + timedelta(days=1)
    )
    data_model.append(data_date_time_tomorrow)
    data_shopping_list2 = ShoppingListEntity(date_time=data_date_time_tomorrow)
    data_model.append(data_shopping_list2)

    # start code block to test
    album = Album.resolve_from_text("the new Taylor Swift album")
    Music.play_music(album=album)

    date_time = DateTime.resolve_from_text("today")
    shopping_lists = Shopping.find_shopping_lists(date_time=date_time)
    Responder.respond(response=shopping_lists)
    # end code block to test

    # assertions
    test_results = {}
    actual = data_model.get_data(MusicEntity)
    expected = [{"album": data_album}]
    entity_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([ShoppingListEntity]))
    actual = next(iterator, None)
    expected = [data_shopping_list1]
    response_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient}]
    entity_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_4():
    """
    Give me directions to Navy pier in Chicago and tell me what the current traffic is looking like.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="Navy pier in Chicago", value="Navy pier in Chicago")
    data_model.append(data_location)
    data_directions = NavigationDirectionEntity(destination=data_location)
    data_model.append(data_directions)
    data_traffic_info = NavigationTrafficInfoEntity(destination=data_location)
    data_model.append(data_traffic_info)

    # start code block to test
    destination = Location.resolve_from_text("Navy pier in Chicago")
    navigation_directions = Navigation.find_directions(destination=destination)
    Responder.respond(response=navigation_directions)

    traffic_info = Navigation.find_traffic_info(destination=destination)
    Responder.respond(response=traffic_info)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_directions]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationTrafficInfoEntity]))
    actual = next(iterator, None)
    expected = [data_traffic_info]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_5():
    """
    Check the next time Blink 182 will be in Chicago and tell me the ticket prices.
    """
    # test data
    data_model = DataModel(reset=True)
    data_event_name = EventName(text="Blink 182")
    data_model.append(data_event_name)
    data_location = Location(text="in Chicago")
    data_model.append(data_location)
    data_event = EventEntity(event_name=data_event_name, location=data_location)
    data_model.append(data_event)
    data_tickets = EventTicketEntity(event_name=data_event_name, location=data_location)
    data_model.append(data_tickets)

    # start code block to test
    event_name = EventName.resolve_from_text("Blink 182")
    location = Location.resolve_from_text("in Chicago")
    events = Calendar.find_events(event_name=event_name, location=location)
    Responder.respond(response=events)

    tickets = Calendar.find_events_tickets(event_name=event_name, location=location)
    Responder.respond(response=tickets)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([EventTicketEntity]))
    actual = next(iterator, None)
    expected = [data_tickets]
    response_assertions(expected, actual, test_results)

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
    Calendar.schedule_event(date_time=date_time, location=location)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "person_reminded": data_contact,
            "date_time": data_date_time_tomorrow,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(EventEntity)
    expected = [{"date_time": data_date_time_noon, "location": data_location}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_7():
    """
    Can you place an order for two turkeys to arrive the 22nd, and remind me about it on the 21st?
    """
    # test data
    data_model = DataModel(reset=True)
    data_amount = Amount(text="two", value=2)
    data_model.append(data_amount)
    data_product_name = ProductName(text="turkeys")
    data_model.append(data_product_name)
    data_date_time_22 = DateTime(text="22nd", value=datetime(2022, 11, 22))
    data_model.append(data_date_time_22)
    data_contact = Contact(text="me", value="me")
    data_model.append(data_contact)
    data_date_time_21 = DateTime(text="21st", value=datetime(2022, 11, 21))
    data_model.append(data_date_time_21)

    # start code block to test
    amount = Amount.resolve_from_text("two")
    product_name = ProductName.resolve_from_text("turkeys")
    date_time = DateTime.resolve_from_text("22nd")
    order = Shopping.order(
        product_name=product_name, amount=amount, date_time=date_time
    )

    date_time = DateTime.resolve_from_text("21st")
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_entity(order)
    Reminders.create_reminder(
        date_time=date_time, person_reminded=person_reminded, content=content
    )
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(OrderEntity)
    expected = [
        {
            "product_name": data_product_name,
            "amount": data_amount,
            "date_time": data_date_time_22,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [
        {
            "date_time": data_date_time_21,
            "person_reminded": data_contact,
            "content": Content(value=order),
        }
        for order in data_model.get_data(OrderEntity)
    ]
    entity_assertions(expected, actual, test_results)

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
    data_estimated_arrival = NavigationEstimatedArrivalEntity(
        destination=data_location, arrival_date_time=data_date_time_8pm
    )
    data_model.append(data_estimated_arrival)
    data_date_time_tonight = DateTime(
        text="tonight", value=datetime(2022, 11, 13, 18, 00)
    )
    data_model.append(data_date_time_tonight)
    data_weather_forecast = WeatherForecastEntity(date_time=data_date_time_tonight)
    data_model.append(data_weather_forecast)

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

    iterator = iter(data_model.get_response([NavigationEstimatedArrivalEntity]))
    actual = next(iterator, None)
    expected = [data_estimated_arrival]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

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
    data_recipient = Contact(text="Grandpa", value="Grandpa")
    data_model.append(data_recipient)
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
    Messages.send_message(recipient=recipient, content=content)

    content = Content.resolve_from_entity(weather_forecasts)
    Messages.send_message(recipient=recipient, content=content)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecasts]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_recipient,
            "content": Content(value=[data_weather_forecasts]),
        },
    ]
    entity_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(TimerEntity)
    expected = [
        {
            "duration": data_duration,
        }
    ]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(MessageEntity)
    expected = [
        {
            "recipient": data_contact,
            "content": data_content,
        }
    ]
    entity_assertions(expected, actual, test_results)


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
    assert_equal(data_reminder.person_reminded, data_person_reminded, test_results)
    assert_equal(data_reminder.content, data_content, test_results)
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

    actual = data_model.get_data(ReminderEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

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
    data_weather_forecast = WeatherForecastEntity(
        date_time=data_date_time, weather_attribute=data_weather_attribute
    )
    data_model.append(data_weather_forecast)
    data_destination = Location(text="home", value="23e 8th st, new york, ny")
    data_model.append(data_destination)
    data_departure_date_time = DateTime(
        text="after 5:00 PM", value=datetime(2022, 11, 14, 17, 1)
    )
    data_model.append(data_departure_date_time)
    data_direction = NavigationDirectionEntity(
        destination=data_destination, departure_date_time=data_departure_date_time
    )
    data_model.append(data_direction)

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

    iterator = iter(data_model.get_response([WeatherForecastEntity]))
    actual = next(iterator, None)
    expected = [data_weather_forecast]
    response_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationDirectionEntity]))
    actual = next(iterator, None)
    expected = [data_direction]
    response_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

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

    actual = data_model.get_data(MessageEntity)
    expected = []
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_16():
    """
    Text my brother I am on my way and also tell me the current traffic conditions.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="my brother", value="Jim Hill")
    data_model.append(data_recipient)
    data_content_omw = Content(
        text="I am on my way",
        value="I am on my way",
    )
    data_model.append(data_content_omw)
    data_navigation_traffic_info = NavigationTrafficInfoEntity()
    data_model.append(data_navigation_traffic_info)

    # start code block to test
    recipient = Contact.resolve_from_text("my brother")
    content = Content.resolve_from_text("I am on my way")
    Messages.send_message(
        recipient=recipient,
        content=content,
    )

    navigation_traffic_info = Navigation.find_traffic_info()
    Responder.respond(response=navigation_traffic_info)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content_omw}]
    entity_assertions(expected, actual, test_results)

    iterator = iter(data_model.get_response([NavigationTrafficInfoEntity]))
    actual = next(iterator, None)
    expected = [data_navigation_traffic_info]
    response_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_17():
    """
    Start my shower playlist and text Lucas that I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out.
    """
    # test data
    data_model = DataModel(reset=True)
    data_playlist = Playlist(text="shower playlist")
    data_model.append(data_playlist)
    data_recipient = Contact(text="Lucas")
    data_model.append(data_recipient)
    data_content = Content(
        text="I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out",
        value="I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out",
    )
    data_model.append(data_content)

    # start code block to test
    playlist = Playlist.resolve_from_text("shower playlist")
    Music.play_music(playlist=playlist)

    recipient = Contact.resolve_from_text("Lucas")
    content = Content.resolve_from_text(
        "I'm just now getting in the shower and it will be 15 or 20 minutes until I'm out"
    )
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


def test_18():
    """
    Tell Abe to pick up bread on his way home and set a timer for 60 minutes.
    """
    # test data
    data_model = DataModel(reset=True)
    data_recipient = Contact(text="Abe")
    data_model.append(data_recipient)
    data_content = Content(
        text="pick up bread on his way home",
    )
    data_model.append(data_content)
    data_duration = TimeDuration(text="60 minutes")
    data_model.append(data_duration)

    # start code block to test
    recipient = Contact.resolve_from_text("Abe")
    content = Content.resolve_from_text("pick up bread on his way home")
    Messages.send_message(recipient=recipient, content=content)

    duration = TimeDuration.resolve_from_text("60 minutes")
    Timer.create_timer(duration=duration)
    # end code block to test

    # assertions
    test_results = {}

    actual = data_model.get_data(MessageEntity)
    expected = [{"recipient": data_recipient, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    actual = data_model.get_data(TimerEntity)
    expected = [{"duration": data_duration}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)


def test_19_a():
    """
    Check the weather in Indianapolis, and if it's sunny, text Bob to remind him about the concert today.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="Indianapolis")
    data_model.append(data_location)
    data_weather_attribute = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute,
        location=data_location,
    )
    data_model.append(data_weather_forecast)

    data_recipient = Contact(text="Bob")
    data_model.append(data_recipient)
    data_content = Content(
        text="remind him about the concert today",
    )
    data_model.append(data_content)

    # start code block to test
    location = Location.resolve_from_text("Indianapolis")
    weather_attribute = WeatherAttribute.resolve_from_text("sunny")
    weather_forecasts = Weather.find_weather_forecasts(
        location=location, weather_attribute=weather_attribute
    )
    Responder.respond(response=weather_forecasts)

    weather_attribute = WeatherAttribute.resolve_from_text("sunny")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_attribute=weather_attribute
    )
    test = bool(weather_forecasts)
    if test:
        recipient = Contact.resolve_from_text("Bob")
        content = Content.resolve_from_text("remind him about the concert today")
        Messages.send_message(recipient=recipient, content=content)
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


def test_19_b():
    """
    Check the weather in Indianapolis, and if it's sunny, text Bob to remind him about the concert today.
    """
    # test data
    data_model = DataModel(reset=True)
    data_location = Location(text="Indianapolis")
    data_model.append(data_location)
    data_weather_attribute = WeatherAttribute(text="sunny")
    data_model.append(data_weather_attribute)
    data_weather_attribute_neg = WeatherAttribute(text="rain")
    data_model.append(data_weather_attribute_neg)
    data_weather_forecast = WeatherForecastEntity(
        weather_attribute=data_weather_attribute_neg,
        location=data_location,
    )
    data_model.append(data_weather_forecast)

    data_recipient = Contact(text="Bob")
    data_model.append(data_recipient)
    data_content = Content(
        text="remind him about the concert today",
    )
    data_model.append(data_content)

    # start code block to test
    location = Location.resolve_from_text("Indianapolis")
    weather_forecasts = Weather.find_weather_forecasts(location=location)
    Responder.respond(response=weather_forecasts)

    weather_attribute = WeatherAttribute.resolve_from_text("sunny")
    weather_forecasts = utils.filter(
        weather_forecasts, weather_attribute=weather_attribute
    )
    test = bool(weather_forecasts)
    if test:
        recipient = Contact.resolve_from_text("Bob")
        content = Content.resolve_from_text("remind him about the concert today")
        Messages.send_message(recipient=recipient, content=content)
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
    data_directions = NavigationDirectionEntity(
        destination=data_destination2,
    )
    data_model.append(data_directions)

    data_recipient = Contact(text="Mike")
    data_model.append(data_recipient)
    data_content = Content(
        text="meet me there in a half hour",
    )
    data_model.append(data_content)

    # start code block to test
    destinations = Location.resolve_many_from_text("movie theater")
    destinations = utils.sort(destinations, "nearest")
    destination = utils.first(destinations)
    navigation_directions = Navigation.find_directions(
        destination=destination,
    )
    Responder.respond(response=navigation_directions)

    recipient = Contact.resolve_from_text("Mike")
    content = Content.resolve_from_text("meet me there in a half hour")
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


def test_21():
    """
    Check my calendar for when my aunt's birthday is this month and then set a reminder for three days before, so I can remember to buy a gift.
    """
    # test data
    data_model = DataModel(reset=True)
    data_calendar = EventCalendar(text="my calendar")
    data_model.append(data_calendar)
    data_event_name = EventName(
        text="my aunt's birthday", value="Auntie Rachel's Birthday"
    )
    data_model.append(data_event_name)
    data_date_time = DateTime(text="this month", value=datetime(2022, 11, 8, 00, 00))
    data_model.append(data_date_time)
    data_event = EventEntity(
        event_name=data_event_name,
        date_time=data_date_time,
        event_calendar=data_calendar,
    )
    data_model.append(data_event)

    data_date_time2 = DateTime(
        text="three days before", value=datetime(2022, 11, 5, 00, 00)
    )
    data_model.append(data_date_time2)
    data_content = Content(text="remember to buy a gift")
    data_model.append(data_content)

    # start code block to test
    event_calendar = EventCalendar.resolve_from_text("my calendar")
    event_name = EventName.resolve_from_text("my aunt's birthday")
    date_time = DateTime.resolve_from_text("this month")
    calendar_events = Calendar.find_events(
        event_name=event_name, date_time=date_time, event_calendar=event_calendar
    )
    Responder.respond(response=calendar_events)

    content = Content.resolve_from_text("remember to buy a gift")
    date_time = DateTime.resolve_from_text("three days before")
    Reminders.create_reminder(content=content, date_time=date_time)
    # end code block to test

    # assertions
    test_results = {}

    iterator = iter(data_model.get_response([EventEntity]))
    actual = next(iterator, None)
    expected = [data_event]
    response_assertions(expected, actual, test_results)

    actual = data_model.get_data(ReminderEntity)
    expected = [{"date_time": data_date_time2, "content": data_content}]
    entity_assertions(expected, actual, test_results)

    assert_test(test_results)
