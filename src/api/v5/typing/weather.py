from __future__ import annotations
from abc import abstractclassmethod
from exceptions.resolvable import Resolvable
from typing.generic import Entity, DateTime, Location
from typing import Callable, Optional


class WeatherAttribute(Entity, Resolvable):
    pass


class WeatherTemperature(Entity, Resolvable):
    pass


class WeatherForecast(Entity):
    date_time: DateTime
    location: Location
    temperature: WeatherTemperature
    weather_attribute: WeatherAttribute
    
    @abstractclassmethod
    def get_predicate(
        WeatherForecast, 
        date_time: Optional[DateTime] = None, 
        location: Optional[Location] = None,
        temperature: Optional[WeatherTemperature] = None,
        weather_attribute: Optional[WeatherAttribute] = None
    ) -> Callable[[WeatherForecast], bool]:
        raise NotImplementedError
    
    