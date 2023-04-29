from abc import abstractmethod
from model import Model
from operators import ComparisonOperator
from arguments import Location, DateTime, WeatherTemperature, WeatherCondition
from typing import Callable, Optional, Iterator
from entity import WeatherEntity


class WeatherModel(Model):
    def __iter__(self) -> Iterator[WeatherEntity]:
        raise NotImplementedError()

    @abstractmethod
    def get_predicate(
        self,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        temperature: Optional[WeatherTemperature] = None,
        weather_condition: Optional[WeatherCondition] = None,
        op: ComparisonOperator = ComparisonOperator.EQ,
    ) -> Callable[[WeatherEntity], bool]:
        raise NotImplementedError


