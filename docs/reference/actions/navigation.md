# Navigation

## `Navigation.find_directions`

This API can support a user request for getting directions from a specific origin to a destination at a specific time.

``` py
Navigation.find_directions(
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
| `nav_travel_method` | `NavTravelMethod` | Yes | Navigation travel method. Defaults to car driving, so use it only in case the travel of method is not a car. |

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
navigation_directions = Navigation.find_directions(
    origin=origin, 
    destination=destination, 
    avoid_nav_road_condition=avoid_nav_road_condition
)
Responder.respond(response=navigation_directions)
```

## `Navigation.find_distance`

This API can support a user request for getting directions from a specific origin to a destination at a specific time.

``` py
Navigation.find_distance(
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
navigation_distance = Navigation.find_distance(
    origin=origin,
    destination=destination
)
Responder.respond(response=navigation_distance)
```

## `Navigation.find_duration`

This API can support a user request for estimating the duration for travelling from one place to another.

``` py
Navigation.find_duration(
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
navigation_duration = Navigation.find_duration(
    destination=destination, 
    nav_travel_method=nav_travel_method
)
Responder.respond(response=navigation_duration)
```

## `Navigation.find_estimated_arrival`

This API can support a user request for estimating an arrival time to a place.

``` py
Navigation.find_estimated_arrival(
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
navigation_estimated_arrival = Navigation.find_estimated_arrival(
    destination=destination, 
    departure_date_time=departure_date_time,
    arrival_date_time=arrival_date_time
)
Responder.respond(response=navigation_estimated_arrival)
```

## `Navigation.find_estimated_departure`

This API can support a user request for estimating departure information from a place.

``` py
Navigation.find_estimated_departure(
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
navigation_estimated_departure = Navigation.find_estimated_departure(
    destination=destination, 
    origin=origin,
    arrival_date_time=arrival_date_time
)
Responder.respond(response=navigation_estimated_departure)
```

## `Navigation.find_traffic_info`

This API can support a user request for information on traffic conditions.

``` py
Navigation.find_traffic_info(
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
traffic_infos = Navigation.find_traffic_info(
    date_time=date_time,
    location=location
)
Responder.respond(response=traffic_infos)
```
