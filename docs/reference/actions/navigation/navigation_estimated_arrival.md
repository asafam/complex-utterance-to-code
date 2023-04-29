# NavigationEstimatedArrival

## `NavigationEstimatedArrival.find`

This API can support a user request for estimating an arrival time to a place.

``` py
NavigationEstimatedArrival.find(
    origin: Optional[Location],
    destination: Optional[Location],
    departure_date_time: Optional[DateTime],
    arrival_date_Time: Optional[DateTime],
    avoid_nav_road_condition: Optional[NavRoadCondition],
    nav_travel_method: Optional[NavTravelMethod]
) : List[NavigationEstimatedArrivalEntity]
```

**Arguments**

| Name          | Type          | Optional    | Description                              |
| ------------- | ------------- | ----------- | --------------------------------------- |
| `origin`      | `Location`    | Yes         | Origin object                            |
| `destination` | `Location`    | Yes         | Destination object                       |
| `departure_date_time`   | `DateTime`    | Yes        | Date/time of departure    |
| `arrival_date_time`   | `DateTime`    | Yes        | Required Date/time for arrival    |
| `avoid_nav_road_condition` | `NavRoadCondition` | Yes | Navigation road condition to avoid |
| `nav_travel_method` | `NavTravelMethod` | Yes | Navigation method |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[NavigationEstimatedArrivalEntity]`    | A list of `NavigationEstimatedArrivalEntity` objects that provides the estimated arrival information, like arrival time, to a destination. This list is returned sorted by default according to the app specific sorting criteria. |

**Example**

{==

Will traffic make me late for work at 5pm if I leave now

==}

``` py
destination = Location.resolve_from_text("work")
arrival_date_time = DateTime.resolve_from_text("5pm")
departure_date_time = DateTime.resolve_from_text("now")
navigation_estimated_arrival = NavigationEstimatedArrival.find(
    destination=destination, 
    departure_date_time=departure_date_time,
    arrival_date_time=arrival_date_time
)
Responder.respond(response=navigation_estimated_arrival)
```
