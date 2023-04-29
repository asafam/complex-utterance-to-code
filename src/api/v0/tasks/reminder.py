from tasks.task import Task
from entities.reminder import Reminder


class ReminderTask(Task):
    
    def find(cls, query: dict[str, str]) -> list[Reminder]:
        pass
    
    def findOne(cls, query: dict[str, str]) -> Reminder:
        pass
    
    def create (cls, params: dict[str, str]) -> Reminder:
        pass
    
    def update(cls, query: dict[str, str], params: dict[str, str]) -> int:
        pass