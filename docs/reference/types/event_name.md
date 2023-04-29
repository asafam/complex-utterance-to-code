# EventName

## `EventName.resolve_from_text`

This API allows us to resolve a calendar event name from a given user input.

``` py
EventName.resolve_from_text(
    text: str
) : EventName
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual description of the event name    |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `EventName`    | `EventName` object based on the `text` parameter to this function. |

**Example**

A `EventName` is the reference to name or title of calendar meetings.

{==

Do I have a townhall meeting this Friday on my work calendar?

==}

``` py
event_name = EventName.resolve_from_text("a townhall meeting")
```
