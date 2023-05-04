from abc import abstractclassmethod
from typing import List, Union, Optional
from entities.generic import *
from entities.clock import *
from entities.music import *
from providers.data_model import DataModel


class Timer:
    @classmethod
    def create_timer(
        cls,
        duration,
        date_time: Optional[DateTime] = None,
    ) -> TimerEntity:
        timer = TimerEntity(
            date_time=date_time,
            duration=duration,
        )
        data_model = DataModel()
        data_model.append(timer)
        return timer

    @abstractclassmethod
    def pause(
        cls,
        timer: Optional[TimerEntity] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractclassmethod
    def restart(
        cls,
        timer: Optional[TimerEntity] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractclassmethod
    def stop(
        cls,
        timer: Optional[TimerEntity] = None,
    ) -> bool:
        raise NotImplementedError


class Alarm:
    @classmethod
    def create_alarm(
        cls,
        date_time: Optional[DateTime] = None,
        song: Optional[Song] = None,
        content: Optional[Content] = False,
    ) -> AlarmEntity:
        alarm = AlarmEntity(date_time=date_time, song=song, content=content)
        data_model = DataModel()
        data_model.append(alarm)
        return alarm
