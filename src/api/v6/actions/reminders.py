from typing import Any, List, Mapping, Union, Optional
from entities.resolvable import Resolvable
from entities.generic import *
from entities.reminder import Content, ReminderEntity
from entities.calendar import CalendarEvent
from exceptions.exceptions import UnderspecificationException
from providers.data_model import DataModel


class Reminders(Resolvable):
    @classmethod
    def create_reminder(
        cls,
        content: Content,
        person_reminded: Optional[Contact] = None,
        date_time: Optional[DateTime] = None,
        calendar_event: Optional[CalendarEvent] = None,
        recovered_args: Optional[Mapping[str, Any]] = None,
    ) -> ReminderEntity:
        if not content:
            payload = {
                "date_time": date_time,
                "person_reminded": person_reminded,
                "content": content,
                "calendar_event": calendar_event,
                "recovered_args": recovered_args,
            }
            raise UnderspecificationException(
                payload=payload,
                recovery_prompt="What should be reminded?",
                message="content argument is missing",
            )
        reminder = ReminderEntity(
            date_time=date_time,
            person_reminded=person_reminded,
            content=content,
        )
        data_model = DataModel()
        data_model.append(reminder)
        return reminder

    # @exception_handler
    @classmethod
    def find_reminders(
        cls,
        person_reminded: Optional[Contact] = None,
        date_time: Optional[DateTime] = None,
        content: Optional[Content] = None,
    ) -> List[ReminderEntity]:
        data_model = DataModel()
        data = data_model.get_data(ReminderEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.data.get("date_time") in date_time]
            else:
                data = [x for x in data if x.data.get("date_time") == date_time]

        if person_reminded:
            data = [x for x in data if x.data.get("person_reminded") == person_reminded]

        if content:
            data = [x for x in data if x.data.get("content") == content]

        return data

    @classmethod
    def delete_reminders(
        cls, reminders: Union[ReminderEntity, List[ReminderEntity]]
    ) -> bool:
        data_model = DataModel()
        data = data_model.get_data(ReminderEntity)
        if reminders:
            if type(reminders) == list:
                data = [x for x in data if x not in reminders]
            else:
                data = [x for x in data if x != reminders]

        return data
