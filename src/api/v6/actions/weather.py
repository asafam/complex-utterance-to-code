from abc import abstractclassmethod
from typing import List, Optional, List, Union
from entities.generic import DateTime, Location
from entities.weather import *
from providers.data_model import DataModel


class Weather:
    @classmethod
    def find_weather_forecasts(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        weather_attribute: Optional[WeatherAttribute] = None,
        weather_temperature_unit: Optional[WeatherTemperature] = None,
    ) -> List[WeatherForecastEntity]:
        data_model = DataModel()
        data = data_model.get_data(WeatherForecastEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        if weather_attribute:
            data = [x for x in data if x.weather_attribute == weather_attribute]

        if weather_temperature_unit:
            data = [
                x
                for x in data
                if x.weather_temperature_unit == weather_temperature_unit
            ]

        return data
