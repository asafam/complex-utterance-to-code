from abc import abstractclassmethod
from typing import List, Union, Optional
from entities.resolvable import Resolvable
from entities.generic import *
from entities.message import *
from entities.app import App
from providers.data_model import DataModel


class Messages(Resolvable):
    @classmethod
    def find_messages(
        cls,
        date_time: Optional[DateTime] = None,
        sender: Optional[Contact] = None,
        recipient: Optional[Contact] = None,
        content: Optional[Content] = None,
        message_status: Optional[MessageStatus] = None,
        message_content_type: Optional[MessageContentType] = None,
        app: Optional[App] = None,
    ) -> List[MessageEntity]:
        data_model = DataModel()
        data = data_model.get_data(MessageEntity)
        if date_time:
            data = [x for x in data if x.date_time == date_time]

        if sender:
            data = [x for x in data if x.sender == sender]

        if recipient:
            data = [x for x in data if x.recipient == recipient]

        if content:
            data = [x for x in data if x.content == content]

        if message_status:
            data = [x for x in data if x.message_status == message_status]

        if message_content_type:
            data = [x for x in data if x.message_content_type == message_content_type]

        if app:
            data = [x for x in data if x.app == app]

        return data

    @classmethod
    def send_message(
        cls,
        recipient: Contact,
        content: Optional[Content] = None,
        date_time: Optional[DateTime] = None,
        message_content_type: Optional[MessageContentType] = None,
    ) -> MessageEntity:
        message = MessageEntity(
            date_time=date_time,
            recipient=recipient,
            content=content,
            message_content_type=message_content_type,
        )
        data_model = DataModel()
        data_model.append(message)
        return message

    @classmethod
    def delete_messages(
        cls, messages: Union[MessageEntity, List[MessageEntity]]
    ) -> None:
        data_model = DataModel()
        if isinstance(messages, MessageEntity):
            messages = [messages]

        for message in messages:
            data_model.delete(message)
