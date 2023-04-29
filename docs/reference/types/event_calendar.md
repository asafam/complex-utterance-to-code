# EventCalendar

## `EventCalendar.resolve_from_text`

This API allows us to resolve a calendar name listing an event from a given user input.

``` py
EventCalendar.resolve_from_text(
    text: str
) : EventCalendar
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual EventCalendar description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `EventCalendar`    | `EventCalendar` object based on the `text` parameter to this function. |

**Example**

A `EventCalendar` is the name of the calendar journey to search or create meeting in.

{==

Do I have a townhall meeting this Friday on my work calendar?

==}

``` py
event_calendar = EventCalendar.resolve_from_text("my work calendar")
```

## `EventCalendar.resolve_many_from_text`

In some cases it will be required to resolve a group of calendar names.

``` py
EventCalendar.resolve_many_from_text(
    text: str
) : List[EventCalendar]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual EventCalendar description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[EventCalendar]`    | A list of `EventCalendar` objects based on the `text` parameter to this function. |

**Example**

A `EventCalendar` is the name of the calendar journey to search or create meeting in.

{==

Search my kids' calendars for any activity tomorrow at 6 pm.

==}

``` py
event_calendars = EventCalendar.resolve_many_from_text("my kids' calendars")
```
