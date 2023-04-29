# Weather

## `Weather.find_weather_forecasts`

This API provides us the weather forecasts.

``` py
Weather.find_weather_forecasts(
    date_time: Optional[DateTime] | List[DateTime],
    location: Optional[Location],
    weather_attribute: Optional[WeatherAttribute],
    weather_temperature_unit: Optional[WeatherTemperatureUnit]
) : List[WeatherEntity]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `date_time`        | `DateTime | List[DateTime]`  | Yes        | Date and time for the weather. An input of         |
| `location`        | `Location`  | Yes        | Location for the weather        |
| `weather_attribute`        | `WeatherAttribute`  | Yes        | Weather attribute to look for in the weather forecasts        |
| `weather_temperature_unit`        | `WeatherTemperatureUnit`  | Yes        | Weather temperature unit to be used in the weather query        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[WeatherEntity]`    | List of `WeatherEntity` objects. Each `WeatherEntity` provides the requested weather forecast for a time frame (e.g. for each day). |

**Example**

This query should return a report by the virtual assistant upon rain tonight.

!!! note
    Please note that some argument are unspecified and in that case the implementation of this method assume their value. For example, `Location` is not specified and therefore the system assumes the location for the weather forecasts.

{==

Is it raining tonight?

==}

``` py
weather_attribute = WeatherAttribute.resolve_from_text("raining")
date_time = DateTime.resolve_from_text("tonight")
weather_forecasts = Weather.find_weather_forecasts(
    weather_attribute=weather_attribute,
    date_time=date_time
)
response = weather_forecasts
Responder.respond(response=response)
```
