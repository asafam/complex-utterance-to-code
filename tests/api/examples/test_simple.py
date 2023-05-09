from entities.reminder import ReminderEntity
from entities.shopping import *
from entities.weather import WeatherAttribute, WeatherForecastEntity
from actions.reminders import Reminders
from actions.responder import Responder
from actions.shopping import Shopping
from actions.weather import Weather
from providers.data_model import DataModel
from entities.generic import *
from datetime import datetime


def test_simple1():
    """
    Is it going to drizzle this weekend?
    """
    # test data
    data_model = DataModel(reset=True)
    data_date_time1 = DateTime(text="this weekend", value=datetime(2022, 10, 8, 0, 0))
    data_date_time2 = DateTime(text="this weekend", value=datetime(2022, 10, 9, 0, 0))
    data_date_time3 = DateTime(text="Sunday", value=datetime(2022, 10, 10, 0, 0))
    data_model.append(data_date_time1)
    data_model.append(data_date_time2)
    data_weather_attribute = WeatherAttribute(text="drizzle", value="rain")
    data_weather_attribute_x = WeatherAttribute(text="cloudy", value="cloudy")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time1, weather_attribute=data_weather_attribute
        )
    )
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time2, weather_attribute=data_weather_attribute
        )
    )
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time3, weather_attribute=data_weather_attribute_x
        )
    )

    # code block to test
    date_time = DateTime.resolve_many_from_text("this weekend")
    weather_attribute = WeatherAttribute.resolve_from_text("drizzle")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time, weather_attribute=weather_attribute
    )
    Responder.respond(response=weather_forecasts)

    #  assertion tests
    data_weather_forecasts_list = data_model.get_response([WeatherForecastEntity])
    assert len(data_weather_forecasts_list) > 0
    data_weather_forecasts = data_weather_forecasts_list[-1]
    assert len(list(data_weather_forecasts)) == 2
    assert list(data_weather_forecasts)[0].date_time == data_date_time1
    assert list(data_weather_forecasts)[0].weather_attribute == data_weather_attribute
    assert list(data_weather_forecasts)[1].date_time == data_date_time2
    assert list(data_weather_forecasts)[1].weather_attribute == data_weather_attribute


def test_simple2():
    """
    Delete reminder to return library books
    """
    # test data
    data_model = DataModel(reset=True)
    data_content = Content(text="return library books", value="return library books")
    data_model.append(data_content)
    data_model.append(ReminderEntity(content=data_content))

    # code block to test
    content = Content.resolve_from_text("return library books")
    reminders = Reminders.find_reminders(content=content)
    Reminders.delete_reminders(reminders=reminders)

    #  assertion tests
    data_reminders = data_model.get_response(ReminderEntity)
    assert len(data_reminders) == 0


def test_simple0():
    """
    Check the availability of Pepsi at Walmart and also check it at Walgreens.
    """
    # test data
    data_model = DataModel(reset=True)
    data_product_name = ProductName(text="Pepsi", value="Pepsi")
    data_model.append(data_product)
    data_location1 = DateTime(text="Walmart", value="Walmart")
    data_model.append(data_location1)
    data_location2 = DateTime(text="Walgreens", value="Walgreens")
    data_model.append(data_location2)
    data_model.append(ProductEntity(product_name=data_product, location=data_location1))
    data_model.append(ProductEntity(product_name=data_product, location=data_location2))

    # start code block to test
    results = []

    product_name = ProductName.resolve_from_text("Pepsi")
    location = DateTime.resolve_from_text("Walmart")
    products = Shopping.find_products(product_name=product_name, location=location)
    results += products

    location = DateTime.resolve_from_text("Walgreens")
    products = Shopping.find_products(product_name=product_name, location=location)
    results += products

    Responder.respond(response=results)
    # end code block to test

    # assertions
    data_products_list = data_model.get_data(ProductEntity)
    assert len(data_products_list) == 2
    data_products = data_products_list
    assert data_products[0].product_name == data_product
    assert data_products[0].location == data_location1
    assert data_products[1].product_name == data_product
    assert data_products[1].location == data_location2
