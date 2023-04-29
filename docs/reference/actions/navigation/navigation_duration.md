# NavigationDuration

## `NavigationDuration.find`

This API can support a user request for estimating the duration for travelling from one place to another.

``` py
NavigationDuration.find(
    origin: Optional[Location],
    destination: Optional[Location],
    departure_date_time: Optional[DateTime],
    avoid_nav_road_condition: Optional[NavRoadCondition],
    nav_travel_method: Optional[NavTravelMethod]
) : List[NavigationDurationEntity]
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
| `NavigationDurationEntity`    | A list of `NavigationDurationEntity` objects that provide the estimated travel duration response. |

**Example**

{==

How long is my drive to Reno, Nevada?

==}

``` py
destination = Location.resolve_from_text("Reno, Nevada")
nav_travel_method = DateTime.resolve_from_text("drive")
navigation_duration = NavigationDuration.find(
    destination=destination, 
    nav_travel_method=nav_travel_method
)
Responder.respond(response=navigation_duration)
```

