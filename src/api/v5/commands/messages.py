from abc import abstractclassmethod
from typing import Iterable, Union, Optional
from api.v5.exceptions.resolvable import Resolvable
from typing.generic import Contact, DateTime, Entity
from typing.message import Message, Content


class MessagesCommand(Resolvable):
    @abstractclassmethod
    def send_message(
        cls,
        recipient: Contact,
        exact_content: Content,
        date_time: Optional[DateTime] = None
    ) -> Message:
        raise NotImplementedError
    
    @abstractclassmethod
    def delete_messages(
        cls,
        messages: Union[Message, Iterable[Message]]
    ) -> Message:
        raise NotImplementedError
