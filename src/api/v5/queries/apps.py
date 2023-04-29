from abc import abstractclassmethod
from typing import Iterable, Optional
from typing.generic import Contact, DateTime
from typing.apps import AppName, App


class AppsQuery():
    
    @abstractclassmethod
    def get_apps(
        cls,
        app_name: Optional[AppName] = None,
    ) -> Iterable[App]:
        raise NotImplementedError
