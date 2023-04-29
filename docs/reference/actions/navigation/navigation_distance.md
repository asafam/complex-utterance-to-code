# NavigationDistance

## `NavigationDistance.find`

This API can support a user request for getting directions from a specific origin to a destination at a specific time.

``` py
Weather.find(
    origin: Optional[Location],
    destination: Optional[Location],
    departure_date_time: Optional[DateTime],
    avoid_nav_road_condition: Optional[NavRoadCondition],
    nav_travel_method: Optional[NavTravelMethod]
) : List[NavigationDistanceEntity]
```

**Arguments**

| Name          | Type          | Optional    | Description                              |
| ------------- | ------------- | ----------- | --------------------------------------- |
| `origin`      | `Location`    | Yes         | Origin object                            |
| `destination` | `Location`    | Yes         | Destination object                       |
| `departure_date_time`   | `DateTime`    | Yes        | Required Date/time for departure    |
| `avoid_nav_road_condition` | `NavRoadCondition` | Yes | NavigationDistance road condition to avoid |
| `nav_travel_method` | `NavTravelMethod` | Yes | NavigationDistance method |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[NavigationDistanceEntity]`    | A list of `NavigationDistanceEntity` objects, which are sorted by default according to the app defined best routes criteria. |

**Example**

{==

How far is New York from Boston?

==}

``` py
origin = Location.resolve_from_text("New York")
destination = Location.resolve_from_text("Boston")
navigation_distance = NavigationDistance.find(
    origin=origin,
    destination=destination
)
Responder.respond(response=navigation_distance)
```
