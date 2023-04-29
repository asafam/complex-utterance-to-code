# EventCategory

## `EventCategory.resolve_from_text`

This API allows us to resolve an event category from a given user input.

``` py
EventCategory.resolve_from_text(
    text: str
) : EventCategory
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual description of the event category       |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `EventCategory` | `EventCategory` object based on the `text` parameter to this function. |

**Example**

{==

Show me Christmas parties for kids in atlanta

==}

``` py
event_category = EventCategory.resolve_from_text("parties")
```
