from abc import abstractclassmethod
from typing import Iterable, Optional
from entities.generic import Contact, DateTime
from typing.message import Message, Content


class MessagesQuery:
    @abstractclassmethod
    def get_messages(
        cls,
        date_time: Optional[DateTime] = None,
        content: Optional[Content] = None,
        sender: Optional[Contact] = None,
        recipient: Optional[Contact] = None,
    ) -> Iterable[Message]:
        raise NotImplementedError
