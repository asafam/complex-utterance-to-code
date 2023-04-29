# Location

## `Location.resolve_from_text`

This API allows us to resolve a location from a given text.

A text can also refer to multiple locations. For example, the text "every drug store in my area" should yield a list of `Location` objects.

``` py
Location.resolve_from_text(
    text: str
) : Location
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual decription of a location         |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `Location`    | `Location` object based on the `text` parameter to this function. |

**Example**

A `Location` can be an address, a city or a country name, or any publicly known place (for example, Times Square).

{==

If I leave now will I get to 37 Spring St by 12:30 pm?

==}

``` py
location = Location.resolve_from_text("37 Spring St")
```

A `Location` can be also be private to the user. It is in the API responsibility to infer a user specific location.

{==

Is it currently raining at home?

==}

``` py
location = Location.resolve_from_text("at home")
```

## `Location.resolve_many_from_text`

This API allows us to resolve multiple locations from a given text. For example, the text "every drug store in my area" should yield a list of `Location` objects.

``` py
Location.resolve_many_from_text(
    text: str
) : List[Location]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual decription of a location         |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[Location]`    | A list of `Location` objects based on the `text` parameter to this function. |

**Example**

A `Location` can be an address, a city or a country name, or any publicly known place (for example, Times Square).

{==

If I leave now will I get to 37 Spring St by 12:30 pm?

==}

``` py
location = Location.resolve_from_text("37 Spring St")
```

A `Location` can be also be private to the user. It is in the API responsibility to infer a user specific location.

{==

Is it currently raining at home?

==}

``` py
location = Location.resolve_from_text("at home")
```

## `Location.resolve_from_entity`

This API allows us to resolve a location from a given entity or list of entities, usually the result of a previous `resolve_from_text()` operation.

``` py
Content.resolve_from_entity(
    entity: Entity | List[Entity]
) : Location | List[Location]
```

**Arguments**

| Name          | Type          | Optional  | Description                                   |
| ------------- | ------------- | --------- | --------------------------------------------- |
| `entity`      | `Entity | List[Entity]`      | No        | An `Entity` object to be transformed to a `Location` |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `Location | List[Location]`    | A location object or a list of `Location` objects based on the `text` parameter to this function. |

**Example**

A `Location` can be be inferred from different objects. One example may be a meeting location or an event venue.

{==

Directions to the Rockets game

==}

``` py
event_name = EventName.resolve_from_text("the Rockets game")
event = Event.find(event_name=event_name)
location = Location.resolve_from_entity(event)
...
```
