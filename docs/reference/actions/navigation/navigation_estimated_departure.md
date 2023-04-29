# NavigationEstimatedDeparture

## `NavigationEstimatedDeparture.find`

This API can support a user request for estimating departure information from a place.

``` py
NavigationEstimatedDeparture.find(
    origin: Optional[Location],
    destination: Optional[Location],
    departure_date_time: Optional[DateTime],
    arrival_date_Time: Optional[DateTime],
    avoid_nav_road_condition: Optional[NavRoadCondition],
    nav_travel_method: Optional[NavTravelMethod]
) : List[NavigationEstimatedDepartureEntity]
```

**Arguments**

| Name          | Type          | Optional    | Description                              |
| ------------- | ------------- | ----------- | --------------------------------------- |
| `origin`      | `Location`    | Yes         | Origin object                            |
| `destination` | `Location`    | Yes         | Destination object                       |
| `departure_date_time`   | `DateTime`    | Yes        | Required Date/time for departure    |
| `arrival_date_time`   | `DateTime`    | Yes        | Date/time of arrival    |
| `avoid_nav_road_condition` | `NavRoadCondition` | Yes | NavigationEstimatedDeparture road condition to avoid |
| `nav_travel_method` | `NavTravelMethod` | Yes | NavigationEstimatedDeparture method |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[NavigationEstimatedDepartureEntity]`    | A list of `NavigationEstimatedDepartureEntity` objects that provides the estimated departure information, like time to depart, from an origin. This list is returned sorted by default according to the app specific sorting criteria. |

**Example**

{==

I have to pick someone up at the airport during rush hour, what time should I leave home in order to meet a 6PM flight

==}

``` py
destination = Location.resolve_from_text("the airport")
origin = Location.resolve_from_text("home")
arrival_date_time = DateTime.resolve_from_text("a 6PM flight")
navigation_estimated_departure = NavigationEstimatedDeparture.find(
    destination=destination, 
    origin=origin,
    arrival_date_time=arrival_date_time
)
Responder.respond(response=navigation_estimated_departure)
```
