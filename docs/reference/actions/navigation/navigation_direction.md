# NavigationDirection

## `NavigationDirection.find`

This API can support a user request for getting directions from a specific origin to a destination at a specific time.

``` py
NavigationDirection.find(
    origin: Optional[Location],
    destination: Optional[Location],
    departure_date_time: Optional[DateTime],
    avoid_nav_road_condition: Optional[NavRoadCondition],
    nav_travel_method: Optional[NavTravelMethod]
) : List[NavigationDirectionEntity]
```

**Arguments**

| Name          | Type          | Optional    | Description                              |
| ------------- | ------------- | ----------- | --------------------------------------- |
| `origin`      | `Location`    | Yes         | Origin object                            |
| `destination` | `Location`    | Yes         | Destination object                       |
| `departure_date_time`   | `DateTime`    | Yes        | Required Date/time for departure    |
| `avoid_nav_road_condition` | `NavRoadCondition` | Yes | Navigation road condition to avoid |
| `nav_travel_method` | `NavTravelMethod` | Yes | Navigation method |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[NavigationDirectionEntity]`    | A list of `NavigationRoute` objects, which are sorted by default according to the app defined best routes criteria. |

**Example**

{==

Get directions from Manhattan to Newark that avoid tollways.

==}

``` py
origin = Location.resolve_from_text("Manhattan")
destination = Location.resolve_from_text("Newark")
avoid_nav_road_condition = NavRoadCondition.resolve_from_text("tollways")
navigation_directions = NavigationDirection.find(
    origin=origin, 
    destination=destination, 
    avoid_nav_road_condition=avoid_nav_road_condition
)
Responder.respond(response=navigation_directions)
```
