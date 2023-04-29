from abc import abstractclassmethod
from task import Task


class TaskFactory:
    
    @abstractclassmethod
    def get_task(cls, id: str) -> Task:
        pass