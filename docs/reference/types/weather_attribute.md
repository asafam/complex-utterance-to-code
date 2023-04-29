# WeatherAttribute

## `WeatherAttribute.resolve_from_text`

This API allows us to resolve a weather attribute or condition from a user input. For example, "stormy", "rain" or "cold" are all weather attributes.

``` py
WeatherAttribute.resolve_from_text(
    text: str
) : WeatherAttribute
```

!!! note
    Weather tempreature unit is represented by `WeatherTemperatureUnit` and is not a weather attribute.

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual WeatherAttribute description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `WeatherAttribute`    | `WeatherAttribute` object based on the `text` parameter to this function. |

**Example**

A `WeatherAttribute` denotes the weather attribute "sunny" in a user command:

{==

Will it be sunny with clear skies this weekend?

==}

``` py
weather_attribute = WeatherAttribute.resolve_from_text("sunny with clear skies")
```

## `WeatherAttribute.resolve_many_from_text`

This API can possibly return a list of `WeatherAttribute` objects given a text input that expresses multiple weather attributes. For example, "any winter weather".

``` py
WeatherAttribute.resolve_from_text(
    text: str
) : List[WeatherAttribute]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual WeatherAttribute description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[WeatherAttribute]`    | A list of `WeatherAttribute` objects based on the `text` parameter to this function. |

**Example**

{==

Are we looking into any non rainy day this week?

==}

``` py
weather_attributes = WeatherAttribute.resolve_many_from_text("any non rainy day")
```
