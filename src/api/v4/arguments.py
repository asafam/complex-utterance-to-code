from __future__ import annotations
from abc import abstractclassmethod
from typing import Iterable, Optional
import entity
from document import Doc


class Argument:
    """
    Markup class
    """


class AppName(Argument):
    @abstractclassmethod
    def resolve_from_document(App, doc: Doc) -> AppName:
        raise NotImplementedError()

    @abstractclassmethod
    def resolve_from_entities(
        Contact, entities: Iterable[entity.AppEntity]
    ) -> AppName:
        raise NotImplementedError()


class Calendar(Argument):
    @abstractclassmethod
    def resolve_from_document(Calendar, doc: Doc) -> Calendar:
        raise NotImplementedError()


class CalendarEvent(Argument):
    @abstractclassmethod
    def resolve_from_document(CalendarEvent, doc: Doc) -> CalendarEvent:
        raise NotImplementedError()


class Contact(Argument):
    @abstractclassmethod
    def resolve_from_document(Contact, doc: Doc) -> Contact:
        raise NotImplementedError()

    @abstractclassmethod
    def resolve_from_entities(
        Contact, entities: Iterable[entity.ContactEntity]
    ) -> Contact:
        raise NotImplementedError()


class DateTime(Argument):
    @abstractclassmethod
    def resolve_from_document(DateTime, doc: Doc) -> DateTime:
        raise NotImplementedError()


class EventAvailability(Argument):
    @abstractclassmethod
    def resolve_from_document(EventAvailability, doc: Doc) -> EventAvailability:
        raise NotImplementedError()


class EventCategory(Argument):
    @abstractclassmethod
    def resolve_from_document(EventCategory, doc: Doc) -> EventCategory:
        raise NotImplementedError()


class Location(Argument):
    @abstractclassmethod
    def resolve_from_document(Location, doc: Doc) -> Location:
        raise NotImplementedError()

    @abstractclassmethod
    def resolve_from_entities(
        Location, entities: Iterable[entity.LocationEntity]
    ) -> Location:
        raise NotImplementedError()


class Reminder(Argument):
    @abstractclassmethod
    def resolve_from_document(Reminder, doc: Doc) -> Reminder:
        raise NotImplementedError()
    
    @abstractclassmethod
    def resolve_from_entities(
        Location, entities: Iterable[entity.ReminderEntity]
    ) -> Reminder:
        raise NotImplementedError()


class Route(Argument):
    @abstractclassmethod
    def resolve_from_document(Route, doc: Doc) -> Route:
        raise NotImplementedError()


class Text(Argument):
    @abstractclassmethod
    def resolve_from_document(Text, doc: Doc) -> Text:
        raise NotImplementedError()

    @abstractclassmethod
    def resolve_from_entities(
        WeatherCondition, entities: Iterable[entity.Entity]
    ) -> Text:
        raise NotImplementedError()


class Timer(Argument):
    @abstractclassmethod
    def resolve_from_document(Timer, doc: Doc) -> Timer:
        raise NotImplementedError()

    @abstractclassmethod
    def resolve_from_entities(Timer, entities: Iterable[entity.TimerEntity]) -> Timer:
        raise NotImplementedError()


class TrafficCondition(Argument):
    @abstractclassmethod
    def resolve_from_document(TrafficCondition, doc: Doc) -> TrafficCondition:
        raise NotImplementedError()


class WeatherCondition(Argument):
    @abstractclassmethod
    def resolve_from_document(WeatherCondition, doc: Doc) -> WeatherCondition:
        raise NotImplementedError()

    @abstractclassmethod
    def resolve_from_entities(
        WeatherCondition, entities: Iterable[entity.WeatherEntity]
    ) -> WeatherCondition:
        raise NotImplementedError()


class WeatherTemperature(Argument):
    @abstractclassmethod
    def resolve_from_document(Temperature, doc: Doc) -> WeatherTemperature:
        raise NotImplementedError()
