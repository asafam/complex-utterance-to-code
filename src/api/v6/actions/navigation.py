from __future__ import annotations
from abc import abstractclassmethod
from entities.generic import DateTime, Location, TimeDuration
from entities.navigation import *
from typing import List, Optional
from providers.data_model import DataModel


class Navigation:
    duration: TimeDuration
    origin: Location
    destination: Location

    @abstractclassmethod
    def find_directions(
        cls,
        destination: Optional[Location],
        origin: Optional[Location] = None,
        departure_date_time: Optional[DateTime] = None,
        avoid_nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationDirectionEntity]:
        data_model = DataModel()
        data = data_model.get_data(NavigationDirectionEntity)
        if destination:
            data = [x for x in data if x.data.get("destination") == destination]

        if origin:
            data = [x for x in data if x.data.get("origin") == origin]

        if departure_date_time:
            data = [
                x
                for x in data
                if x.data.get("departure_date_time") == departure_date_time
            ]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.data.get("avoid_nav_road_condition") == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [
                x for x in data if x.data.get("nav_travel_method") == nav_travel_method
            ]

        return data

    @abstractclassmethod
    def find_distance(
        cls,
        origin: Optional[Location],
        destination: Optional[Location],
        departure_date_time: Optional[DateTime],
        avoid_nav_road_condition: Optional[NavigationRoadCondition],
        nav_travel_method: Optional[NavigationTravelMethod],
    ) -> List[NavigationDistanceEntity]:
        data_model = DataModel()
        data = data_model.get_data(NavigationDistanceEntity)
        if origin:
            data = [x for x in data if x.data.get("origin") == origin]

        if destination:
            data = [x for x in data if x.data.get("destination") == destination]

        if departure_date_time:
            data = [
                x
                for x in data
                if x.data.get("departure_date_time") == departure_date_time
            ]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.data.get("avoid_nav_road_condition") == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [
                x for x in data if x.data.get("nav_travel_method") == nav_travel_method
            ]

        return data

    @abstractclassmethod
    def find_duration(
        cls,
        origin: Optional[Location],
        destination: Optional[Location],
        departure_date_time: Optional[DateTime],
        avoid_nav_road_condition: Optional[NavigationRoadCondition],
        nav_travel_method: Optional[NavigationTravelMethod],
    ) -> List[NavigationDurationEntity]:
        raise NotImplementedError

    @abstractclassmethod
    def find_estimated_arrival(
        cls,
        origin: Optional[Location] = None,
        destination: Optional[Location] = None,
        arrival_date_time: Optional[DateTime] = None,
        avoid_nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationEstimatedArrivalEntity]:
        data_model = DataModel()
        data = data_model.get_data(NavigationEstimatedArrivalEntity)
        if origin:
            data = [x for x in data if x.data.get("origin") == origin]

        if destination:
            data = [x for x in data if x.data.get("destination") == destination]

        if arrival_date_time:
            data = [
                x for x in data if x.data.get("arrival_date_time") == arrival_date_time
            ]

        if avoid_nav_road_condition:
            data = [
                x
                for x in data
                if x.data.get("avoid_nav_road_condition") == avoid_nav_road_condition
            ]

        if nav_travel_method:
            data = [
                x for x in data if x.data.get("nav_travel_method") == nav_travel_method
            ]

        return data

    @abstractclassmethod
    def find_estimated_departure(
        cls,
        origin: Optional[Location],
        destination: Optional[Location],
        departure_date_time: Optional[DateTime],
        arrival_date_Time: Optional[DateTime],
        avoid_nav_road_condition: Optional[NavigationRoadCondition],
        nav_travel_method: Optional[NavigationTravelMethod],
    ) -> List[NavigationEstimatedDepartureEntity]:
        raise NotImplementedError

    @abstractclassmethod
    def find_traffic_info(
        cls,
        location: Optional[Location] = None,
        origin: Optional[Location] = None,
        destination: Optional[Location] = None,
        date_time: Optional[DateTime] = None,
        departure_date_time: Optional[DateTime] = None,
        nav_road_condition: Optional[NavigationRoadCondition] = None,
        nav_travel_method: Optional[NavigationTravelMethod] = None,
    ) -> List[NavigationTrafficInfoEntity]:
        data_model = DataModel()
        data = data_model.get_data(NavigationTrafficInfoEntity)
        if location:
            data = [x for x in data if x.data.get("location") == location]

        if origin:
            data = [x for x in data if x.data.get("origin") == origin]

        if destination:
            data = [x for x in data if x.data.get("destination") == destination]

        if date_time:
            data = [x for x in data if x.data.get("date_time") == date_time]

        if departure_date_time:
            data = [
                x
                for x in data
                if x.data.get("departure_date_time") == departure_date_time
            ]

        if nav_road_condition:
            data = [
                x
                for x in data
                if x.data.get("nav_road_condition") == nav_road_condition
            ]

        if nav_travel_method:
            data = [
                x for x in data if x.data.get("nav_travel_method") == nav_travel_method
            ]

        return data
