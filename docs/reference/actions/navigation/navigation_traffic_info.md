# NavigationTrafficInfo

## `NavigationTrafficInfo.find`

This API can support a user request for information on traffic conditions.

``` py
NavigationTrafficInfo.find(
    location: Optional[Location],
    origin: Optional[Location],
    destination: Optional[Location],
    date_time: Optional[DateTime],
    departure_date_time: Optional[DateTime],
    avoid_nav_road_condition: Optional[NavRoadCondition],
    nav_travel_method: Optional[NavTravelMethod]
) : List[NavigationTrafficInfoEntity]
```

**Arguments**

| Name          | Type          | Optional    | Description                              |
| ------------- | ------------- | ----------- | --------------------------------------- |
| `origin`      | `Location`    | Yes         | Origin object                            |
| `location` | `Location`    | Yes         | Requested location for traffic infomration                       |
| `destination` | `Location`    | Yes         | Destination object                       |
| `date_time` | `DateTime`    | Yes         | Requested date and time for traffic information                       |
| `departure_date_time`   | `DateTime`    | Yes        | Required Date/time for departure    |
| `avoid_nav_road_condition` | `NavRoadCondition` | Yes | NavigationTrafficInfo road condition to avoid |
| `nav_travel_method` | `NavTravelMethod` | Yes | NavigationTrafficInfo method |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[NavigationTrafficInfoEntity]`    | A list of `NavigationTrafficInfoEntity` objects that provides the estimated traffic information. |

**Example**

{==

Is traffic heavy right now in Minneapolis

==}

``` py
date_time = DateTime.resolve_from_text("right now")
location = Location.resolve_from_text("Minneapolis")
traffic_infos = NavigationTrafficInfo.find(
    date_time=date_time,
    location=location
)
Responder.respond(response=traffic_infos)
```
