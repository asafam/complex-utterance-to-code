# Event

Events can be public or private. Public events are for example a concert in the park or a game, where there is a general knowledge about the event and its details. A private event can appear as an entry in the user calendar and include information about the event in a calendar app.

## `Event.find_events`

This API provides us with events information.

``` py
Event.find_events(
    date_time: Optional[DateTime],
    location: Optional[Location],
    event_name: Optional[EventName],
    event_calendar: Optional[EventCalendar],
    app: Optional[Resurce]
) : List[EventEntity]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `date_time`        | `DateTime`  | Yes        | Date and time of the event        |
| `location`        | `Location`  | Yes        | Event location        |
| `event_name`        | `EventName`  | Yes        | The event name        |
| `event_calendar`        | `EventCalendar`  | Yes        | The calendar name where the event should be listed |
| `app`        | `App`  | Yes        | The event app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[EventEntity]`    | List of `EventEntity` objects |

**Example**

{==

When is the Eagles concert with Chris Stapleton coming to Dallas?

==}

``` py
event_name = EventName.resolve_from_text("Eagles concert with Chris Stapleton")
location = Location.resolve_from_text("Dallas")
events = Event.find_events(
    event_name=event_name,
    location=location
)
Responder.respond(response=events)
```

**Example**

{==

Show me my next meeting on my work calendar.

==}

``` py
event_name = EventName.resolve_from_text("next meeting")
event_calendar = EventCalendar.resolve_from_text("my work calendar")
events = Event.find_events(
    event_category=event_category,
    event_calendar=event_calendar
)
events = utils.first(events)
Responder.respond(response=events)
```
