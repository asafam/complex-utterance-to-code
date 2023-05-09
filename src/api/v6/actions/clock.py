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
        duration: Optional[TimeDuration] = None,
        date_time: Optional[DateTime] = None,
    ) -> TimerEntity:
        timer = TimerEntity(
            duration=duration,
            date_time=date_time,
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

    @classmethod
    def update_alarm(
        cls,
        date_time: Optional[DateTime] = None,
        alarm_name: Optional[AlarmName] = None,
    ) -> AlarmEntity:
        alarm = AlarmEntity(date_time=date_time, alarm_name=alarm_name)
        data_model = DataModel()
        data_model.append(alarm)
        return alarm

    @classmethod
    def find_alarms(
        cls,
        date_time: Optional[DateTime],
        alarm_name: Optional[AlarmName],
    ) -> List[AlarmEntity]:
        data_model = DataModel()
        data = data_model.get_data(AlarmEntity)
        if date_time:
            data = [x for x in data if x.date_time == date_time]

        if alarm_name:
            data = [x for x in data if x.alarm_name == alarm_name]
            
        return data
