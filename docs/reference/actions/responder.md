# Responder

## `Responder.respond`

Whenever users ask quetions that requires a specific response, or request something to be displayed or read to them - this is where the `Responder` comes handy. It sole role is to deliver the information to the user on screen or on audio.

``` py
Responder.find_events(
    response: Entity
) : None
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `response`        | `Entity|List[Entity]`  | No        | The `Responder` is able to transform any given `Entity` or a list of `Entity` to a user expected response form to the user.  |

!!! note 
    `Entity` is the base class of all entities returned by any of the other actions listed in this reference.

**Returns**

This function does not return.

**Example**

{==

When is the Eagles concert with Chris Stapleton coming to Dallas?

==}

``` py
event_name = ResponderName.resolve_from_text("Eagles concert with Chris Stapleton")
event_category = ResponderCategory.resolve_from_text("concert")
location = Location.resolve_from_text("Dallas")
events = Event.find(
    event_name=event_name,
    event_category=event_category,
    location=location
)
Responder.respond(response=events)
```

**Example**

{==

Show me my next meeting on my work calendar.

==}

``` py
event_category = ResponderCategory.resolve_from_text("meeting")
event_calendar = ResponderCalendar.resolve_from_text("my work calendar")
events = Event.find(
    event_category=event_category,
    event_calendar=event_calendar
)
events = utils.first(events)
Responder.respond(response=events)
```
