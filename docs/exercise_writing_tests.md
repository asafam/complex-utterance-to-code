# Exercise writing tests

Let's test your knowledge of the [Tests](tests.md) tutorial. We will provide you with a user command and you will write the test to match it.

## Exercise 1

Write a test for the following user command:

{==

Check the weather for the 4th of July and send a text to Grandpa that he should come over

==}

??? tip "Hint"

    Required API references for this exercise:

    * [Message](reference/actions/message.md)
    * [Weather](reference/actions/weather.md)

??? question "Solution"

    ```py
    from providers.data_model import DataModel
    from entities.generic import Contact, Content, DateTime
    from entities.weather import WeatherForecastEntity
    from entities.message import MessageEntity

    data_model = DataModel(reset=True)
    # seed data for the 1st command
    data_date_time = DateTime(text="4th of July", value=datettime.now() + timedelta(days=1))
    data_model.append(data_date_time)
    data_model.append(
        WeatherForecastEntity(date_time=data_date_time)
    )
    # seed the data for the 2nd command
    data_recipient = Contact(text="Grandpa")
    data_model.append(data_recipient)
    data_content = Content(text="he should come over")
    data_model.append(data_content)

    # test assertions for the 1st command
    data_weather_forecasts_list = data_model.get_data(WeatherForecast)
    assert len(data_weather_forecasts_list) == 1
    data_weather_forecasts = data_weather_forecasts_list[0]
    assert test_equal(data_weather_forecasts[0].data.get("date_time"), data_date_time)
    # test assertions for the 2nd command
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert test_equal(data_message.data.get("recipient"), data_recipient)
    assert test_equal(data_message.data.get("content"), data_content)
    ```

## Exercise 2

Write a test for the following user command:

{==

If it rains tomorrow message dad that I will be running late.

==}

??? tip "Hint"

    Required API references for this exercise:

    * [Message](reference/actions/message.md)
    * [Weather](reference/actions/weather.md)

??? question "Solution"

    ```py
    from providers.data_model import DataModel
    from entities.generic import Contact, Content, DateTime
    from entities.weather import WeatherAttribute, WeatherForecastEntity

    data_model = DataModel(reset=True)
    # seed data for the condition query
    data_date_time_tomorrow = DateTime(text="tomorrow", value=datettime.now() + timedelta(days=1))
    data_model.append(data_date_time_tomorrow)
    data_weather_attribute = WeatherAttribute(text="rains")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecastEntity(
            date_time=data_date_time_tomorrow,
            weather_attribute=data_weather_attribute
        )
    )
    # seed the data for the executed command
    data_recipient = Contact(text="dad")
    data_model.append(data_recipient)
    data_content = Content(text="I will be running late")
    data_model.append(data_content)

    # test assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 1
    data_message = data_messages[0]
    assert test_equal(data_message.data.get("recipient"), data_recipient)
    assert test_equal(data_message.data.get("content"), data_content)
    ```

    Additional test for the case the condition is not met:

    ```py
    from providers.data_model import DataModel
    from entities.generic import Contact, Content, DateTime
    from entities.weather import WeatherAttribute, WeatherForecastEntity

    data_model = DataModel(reset=True)
    # seed data for the condition query
    data_date_time_tomorrow = DateTime(text="tomorrow", value=datettime.now() + timedelta(days=1))
    data_model.append(data_date_time_tomorrow)
    data_weather_attribute = WeatherAttribute(text="not rain")
    data_model.append(data_weather_attribute)
    data_model.append(
        WeatherForecast(
            date_time=data_date_time_tomorrow,
            weather_attribute=data_weather_attribute
        )
    )
    # seed the data for the executed command
    data_recipient = Contact(text="dad")
    data_model.append(data_recipient)
    data_content = Content(text="I will be running late")
    data_model.append(data_content)

    # test assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 0
    ```

## Exercise 3

Write a test for the following user command:

{==

Text Stacy and Amanda that dinner will be ready in one hour.

==}

??? tip "Hint"

    Required API references for this exercise:

    * [Message](reference/actions/message.md)

??? question "Solution"

    ```py
    from providers.data_model import DataModel
    from entities.generic import Contact, Conten
    from entities.message import MessageEntity

    # test data
    data_model = DataModel(reset=True)
    data_contact_stacy = Contact(text="Stacy")
    data_model.append(data_contact_stacy)
    data_contact_amanda = Contact(text="Amanda")
    data_model.append(data_contact_amanda)
    data_content = Content(
        text="dinner will be ready in one hour"
    )
    data_model.append(data_content)

    # assertions
    data_messages = data_model.get_data(MessageEntity)
    assert len(data_messages) == 2
    assert test_equal(data_messages[0].data.get("recipient"), data_contact_stacy)
    assert test_equal(data_messages[0].data.get("content"), data_content)
    assert test_equal(data_messages[1].data.get("recipient"), data_contact_amanda)
    assert test_equal(data_messages[1].data.get("content"), data_content)
    ```

## Exercise 4

Write a test for the following user command:

{==

Send Tyler a text saying hi and send one to Susan too.

==}

??? tip "Hint"

    Required API references for this exercise:

    * [Message](reference/actions/message.md)

??? question "Solution"

    ```py
    from providers.data_model import DataModel
    from entities.generic import Contact, Content
    from entities.message import MessageEntity

    # test data
    data_model = DataModel(reset=True)
    data_contact1 = Contact(text="Tyler")
    data_model.append(data_contact1)
    data_contact2 = Contact(text="Susan")
    data_model.append(data_contact2)
    data_content = Content(text="hi")
    data_model.append(data_content)

    # test assertions
    data_messages = data_model.get_response(MessageEntity)
    assert len(data_messages) == 2
    data_message1 = data_messages[0]
    assert test_equal(data_message1.data.get("recipient"), data_contact1)
    assert test_equal(data_message1.data.get("content"), data_content)
    data_message2 = data_messages[1]
    assert test_equal(data_message2.data.get("recipient"), data_contact2)
    assert test_equal(data_message2.data.get("content"), data_content)
    ```
