from abc import abstractclassmethod
from typing import List, Optional, List, Union
from entities.generic import *
from entities.calendar import *
from providers.data_model import DataModel


class Calendar:
    @classmethod
    def find_events(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
    ) -> List[EventEntity]:
        data_model = DataModel()
        data = data_model.get_data(EventEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        if event_name:
            data = [x for x in data if x.event_name == event_name]

        if event_calendar:
            data = [x for x in data if x.event_calendar == event_calendar]

        if event_category:
            data = [x for x in data if x.event_category == event_category]

        return data

    @classmethod
    def find_events_tickets(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
        amount: Optional[Amount] = None,
    ) -> List[EventTicketEntity]:
        data_model = DataModel()
        data = data_model.get_data(EventTicketEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        if event_name:
            data = [x for x in data if x.event_name == event_name]

        if event_calendar:
            data = [x for x in data if x.event_calendar == event_calendar]

        if event_category:
            data = [x for x in data if x.event_category == event_category]

        if amount:
            data = [x for x in data if x.amount == amount]

        return data

    @classmethod
    def schedule_event(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
    ) -> EventEntity:
        event = EventEntity(
            date_time=date_time,
            location=location,
            event_name=event_name,
            event_calendar=event_calendar,
            event_category=event_category,
        )
        data_model = DataModel()
        data_model.append(event)
        return event

    @classmethod
    def delete_events(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        event_calendar: Optional[EventCalendar] = None,
        event_category: Optional[EventType] = None,
    ) -> EventEntity:
        data_model = DataModel()
        events = cls.find_events(
            date_time=date_time,
            location=location,
            event_name=event_name,
            event_calendar=event_calendar,
            event_category=event_category,
        )
        for event in events:
            data_model.delete(event)

    @classmethod
    def purchase_tickets(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[EventName] = None,
        amount: Optional[Amount] = None,
    ) -> EventTicketEntity:
        event_ticket = EventTicketEntity(
            date_time=date_time,
            location=location,
            event_name=event_name,
            amount=amount,
        )
        data_model = DataModel()
        data_model.append(event_ticket)
        return event_ticket
