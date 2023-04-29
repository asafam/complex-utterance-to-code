# WeatherTemperatureUnit

## `WeatherTemperatureUnit.resolve_from_text`

This API allows us to resolve a requested temperature unit (like celsius or fahrenheit).

Despite the fact that this function may return `WeatherTemperatureUnit` it is highly unlikely to find an example where a list would be returned.

``` py
WeatherTemperatureUnit.resolve_from_text(
    text: str
) : WeatherTemperatureUnit : List[WeatherTemperatureUnit]
```

!!! note
    Weather tempreature unit is represented by `WeatherTemperatureUnit` and is not a weather attribute.

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual WeatherTemperatureUnit description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `WeatherTemperatureUnit | List[WeatherTemperatureUnit]`    | `WeatherTemperatureUnit` object or a list of `WeatherTemperatureUnit` objects based on the `text` parameter to this function. |

**Example**

A `WeatherTemperatureUnit` denote the weather attribute "sunny" in a user command:

{==

Tell me the weather in fahrenheit.

==}

``` py
weather_temperature_unit = WeatherTemperatureUnit.resolve_from_text("fahrenheit")
```
