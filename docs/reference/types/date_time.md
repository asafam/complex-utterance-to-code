# DateTime

## `DateTime.resolve_from_text`

This API allows us to resolve a date or time decription from a given text.

``` py
DateTime.resolve_from_text(
    text: str
) : DateTime
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual decription of a time description         |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `DateTime`    | `DateTime` object based on the `text` parameter to this function. |

**Example**

A `DateTime` can be a day, a specific time, or any publicly known place (for example, Times Square).

{==

If I leave now will I get to 37 Spring St by 12:30 pm?

==}

``` py
date_time = DateTime.resolve_from_text("now")
```

## `DateTime.resolve_many_from_text`

This API allows us to resolve multiple dates or times from a given text.

``` py
DateTime.resolve_many_from_text(
    text: str
) : List[DateTime]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual decription of a time description         |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[DateTime]`    | A list of `DateTime` objects based on the `text` parameter to this function. |

**Example**

A `DateTime` can be a logical name for multiple days (for example, the weeekend), or a domain knowledge (public o personal) for a group of times (e.g., the weeks we will be on vacation).

{==

What will be the weather during the weekend?

==}

``` py
date_times = DateTime.resolve_many_from_text("the weekend")
```

## `DateTime.resolve_from_entity`

This API allows us to resolve a DateTime from a given entity or list of entities, usually the result of a previous `resolve_from_text()` operation.

``` py
DateTime.resolve_from_entity(
    entity: Entity | List[Entity]
) : DateTime | List[DateTime]
```

**Arguments**

| Name          | Type          | Optional  | Description                                   |
| ------------- | ------------- | --------- | --------------------------------------------- |
| `entity`      | `Entity | List[Entity]`      | No        | An `Entity` object to be transformed to a `DateTime` |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `DateTime | List[DateTime]`    | A DateTime object or a list of `DateTime` objects based on the `text` parameter to this function. |

**Example**

A `DateTime` can be be inferred from different objects. For example, an event time or the estimated time of arrival to a place.

{==

Will there be traffic downtown during the Rockets game?

==}

``` py
event_name = EventName.resolve_from_text("the Rockets game")
event = Event.find(event_name=event_name)
date_time = DateTime.resolve_from_entity(event)
...
```
