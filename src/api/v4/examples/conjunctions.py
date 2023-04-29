from document import Doc
from models.contacts import ContactsModel
from models.navigation import DirectionsModel
from models.locations import LocationsModel
from models.messages import MessagesModel
from models.reminders import RemindersModel
from models.timer import TimerModel
from models.weather import WeatherModel
from commands.reminder import ReminderDeleteCommand
from commands.response import DefaultResponseCommand, VoiceResponseCommand
from commands.timer import TimerPauseCommand, TimerRestartCommand, TimerStopCommand
from arguments import Contact, DateTime, Location, Reminder, Timer, Text


# Example: "Pause the timer, stop it, and restart it"

doc = Doc("Pause the timer, stop it, and restart it")

timer_model = TimerModel(doc.text("the timer"))
timers = iter(timer_model)
the_timer = filter(
    timer_model.get_predicate(timer_name=Timer.resolve_from_document(doc="the timer")),
    timers,
)
the_timer = sorted(the_timer)

command1 = TimerPauseCommand(doc.text("pause the timer"))
command1.call(timer=Timer.resolve_from_entities(entities=the_timer))

command2 = TimerStopCommand(doc.text("stop it"))
command2.call(timer=Timer.resolve_from_entities(entities=the_timer))

command3 = TimerRestartCommand(doc.text("restart it"))
command3.call(timer=Timer.resolve_from_entities(entities=the_timer))


# Example: "Tell me the weather forecast and delete the last reminder"

doc = Doc("Tell me the weather forecast and delete the last reminder")

weather_model = WeatherModel(doc.text("the weather forecast"))
weather = iter(weather_model)
the_weather = filter(weather_model.get_predicate(), weather)
the_weather = sorted(the_weather)

command1 = VoiceResponseCommand(doc.text("Tell me the weather forecast"))
command1.call(content=Text.resolve_from_entities(entities=the_weather))

reminders_model = RemindersModel(doc.text("the last reminder"))
reminders = iter(reminders_model)
reminders = sorted(reminders, key=reminders_model.get_value_extractor(doc.text("last")))
last_reminder = list(reminders)[-1:]

command2 = ReminderDeleteCommand(doc.text("delete the last reminder"))
command2.call(reminders=Reminder.resolve_from_entities(entities=last_reminder))
