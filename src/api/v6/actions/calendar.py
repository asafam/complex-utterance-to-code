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
                data = [x for x in data if x.data.get("date_time") in date_time]
            else:
                data = [x for x in data if x.data.get("date_time") == date_time]

        if location:
            data = [x for x in data if x.data.get("location") == location]

        if event_name:
            data = [x for x in data if x.data.get("event_name") == event_name]

        if event_calendar:
            data = [x for x in data if x.data.get("event_calendar") == event_calendar]

        if event_category:
            data = [x for x in data if x.data.get("event_category") == event_category]

        return data

    @classmethod
    def find_events_tickets(
        cls, events: List[EventEntity], amount: Optional[Amount] = None
    ) -> List[EventTicketEntity]:
        data_model = DataModel()
        data = data_model.get_data(EventTicketEntity)
        if events:
            if type(events) == list:
                data = [x for x in data if x.data.get("event") in events]
            else:
                data = [x for x in data if x.data.get("event") == events]

        if amount:
            data = [x for x in data if x.data.get("amount") == amount]

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
        events: Union[EventEntity, List[EventEntity]],
    ) -> EventEntity:
        data_model = DataModel()
        for event in events:
            data_model.delete(event)

    @classmethod
    def purchase_tickets(
        cls,
        event_tickets: Optional[
            Union[EventTicketEntity, List[EventTicketEntity]]
        ] = None,
        events: Optional[Union[EventEntity, List[EventEntity]]] = None,
        amount: Optional[Amount] = None,
    ) -> EventTicketEntity:
        data_model = DataModel()
        event_tickets = event_tickets or cls.find_events_tickets(
            events=events, amount=amount
        )
        if event_tickets:
            event_tickets = (
                event_ticket if type(event_tickets) == list else [event_tickets]
            )
            for event_ticket in event_tickets:
                data_model.append(event_ticket)
        return event_ticket
