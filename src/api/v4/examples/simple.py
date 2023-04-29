from api.v4.arguments import WeatherCondition
from document import Doc
from models.contacts import ContactsModel
from models.navigation import (
    DirectionsModel,
    EstimateArrivalModel,
    EstimateDepartureModel,
)
from models.locations import LocationsModel
from models.messages import MessagesModel
from models.weather import WeatherModel
from commands.response import DefaultResponseCommand, VoiceResponseCommand
from arguments import Contact, Location, Text, DateTime, Route


"""
Example: "Directions from Monteray to San Francisco"
"""
doc = Doc("Directions from Monteray to San Francisco")

locations_model = LocationsModel(doc.text("Monteray"))
locations = iter(locations_model)
monteray = filter(
    locations_model.get_predicate(
        location=Location.resolve_from_document(doc=doc.text("Monteray"))
    ),
    locations,
)
monteray = sorted(monteray)

locations_model = LocationsModel(doc.text("San Francisco"))
locations = iter(locations_model)
sf = filter(
    locations_model.get_predicate(
        location=Location.resolve_from_document(doc=doc.text("San Francisco"))
    ),
    locations,
)
sf = sorted(sf)

directions_model = DirectionsModel(
    doc.text("Directions from Monteray to San Francisco")
)
directions = iter(directions_model)
directions_sf = filter(
    directions_model.get_predicate(
        source=Location.resolve_from_entities(entities=monteray),
        destination=Location.resolve_from_entities(entities=sf),
    ),
    directions,
)
directions_sf = sorted(directions)

command = DefaultResponseCommand(doc.text("Directions from Monteray to San Francisco"))
command.call(content=Text.resolve_from_entities(entities=directions_sf))


"""
Example: "Tell me the weather in Fairlawn, New Jersey"
"""
doc = Doc("Tell me the weather in Fairlawn, New Jersey")

locations_model = LocationsModel(doc.text("Fairlawn, New Jersey"))
locations = iter(locations_model)
fairlawn_nj = filter(
    locations_model.get_predicate(
        location=Location.resolve_from_document(doc=doc.text("Fairlawn, New Jersey"))
    ),
    locations,
)
fairlawn_nj = sorted(fairlawn_nj)

weather_model = WeatherModel(doc.text("the weather tomorrow in Fairlawn, New Jersey"))
weather = iter(weather_model)
the_weather = filter(
    weather_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("tomorrow")),
        location=Location.resolve_from_entities(entities=fairlawn_nj),
    ),
    weather,
)
the_weather = sorted(the_weather)

command = DefaultResponseCommand(
    doc.text("Tell me the weather in Fairlawn, New Jersey")
)
command.call(content=Text.resolve_from_entities(entities=the_weather))


"""
Example: ”Get the weather in London today and tomorrow”
"""
doc = Doc("Get the weather in London today and tomorrow")

location_model = LocationsModel(doc.text("London"))
locations = iter(location_model)
london = filter(
    location_model.get_predicate(
        location=Location.resolve_from_document(doc=doc.text("London"))
    ),
    locations,
)
london = sorted(london)

weather_model = WeatherModel(doc.text("Directions from Monteray to San Francisco"))
weather = iter(weather_model)
london_weather = filter(
    lambda x: (
        weather_model.get_predicate(
            date_time=DateTime.resolve_from_document(doc=doc.text("today"))
        )(x)
        or weather_model.get_predicate(
            date_time=DateTime.resolve_from_document(doc=doc.text("tomorrow"))
        )(x)
    )
    and weather_model.get_predicate(location=Location.resolve_from_entities(entities=london))(x),
    weather,
)
london_weather = sorted(london_weather)

command = DefaultResponseCommand(
    doc.text("Get the weather in London today and tomorrow")
)
command.call(content=Text.resolve_from_entities(entities=london_weather))


"""
Example: "Check the last message that Kathy sent"
"""
doc = Doc("Check the last message that Kathy sent")

contacts_model = ContactsModel(doc.text("London"))
contacts = iter(contacts_model)
kathy = filter(
    contacts_model.get_predicate(
        contact=Contact.resolve_from_document(doc=doc.text("London"))
    ),
    contacts,
)
kathy = sorted(kathy)

messages_model = MessagesModel(doc.text("the last message that Kathy sent"))
messages = iter(messages_model)
kathy_messages = filter(
    messages_model.get_predicate(sender=Contact.resolve_from_entities(entities=kathy)), messages
)
kathy_messages = sorted(
    kathy_messages, key=messages_model.get_value_extractor(doc.text("last"))
)
kathy_last_messages = list(kathy_messages)[-1:]

command = DefaultResponseCommand(doc.text("Check the last message that Kathy sent"))
command.call(content=Text.resolve_from_entities(entities=kathy_last_messages))


"""
Example: ”Tell me the weather even though it is early”
"""
doc = Doc("Tell me the weather even though it is early")

weather_model = WeatherModel(doc.text("the weather"))
weather = iter(weather_model)
the_weather = filter(weather_model.get_predicate(), weather)
the_weather = sorted(the_weather)

command = VoiceResponseCommand(doc.text("Tell me the weather"))
command.call(content=Text.resolve_from_entities(entities=the_weather))


"""
Example: "If I take 290 what time will I be in Johnson City?"
"""
doc = Doc("If I take 290 what time will I be in Johnson City?")

location_model = LocationsModel(doc.text("Johnson City"))
locations = iter(location_model)
johnson_city = filter(
    location_model.get_predicate(
        location=Location.resolve_from_document(doc="Johnson City")
    ),
    locations,
)
johnson_city = sorted(johnson_city)

estimate_arrival_model = EstimateArrivalModel(
    doc.text("If I take 290 what time will I be in Johnson City?")
)
estimations = iter(estimate_arrival_model)
classs = filter(
    estimate_arrival_model.get_predicate(
        path=Route.resolve_from_document(doc=doc.text("290")),
        destination=Location.resolve_from_entities(entities=johnson_city),
    ),
    estimations,
)
classs = sorted(classs)


"""
Example: "When I need to leave for class to be there at 8 am"
"""
doc = Doc("When I need to leave for class to be there at 8 am")

location_model = LocationsModel(doc.text("class"))
locations = iter(location_model)
classs = filter(
    location_model.get_predicate(location=Location.resolve_from_document(doc="class")),
    locations,
)
classs = sorted(classs)

estimate_model = EstimateDepartureModel(
    doc.text("When I need to leave for class to be there at 8 am")
)
estimations = iter(estimate_model)
classs = filter(
    estimate_model.get_predicate(
        destination=Location.resolve_from_document(doc=classs),
        date_time_arrival=DateTime.resolve_from_document(doc=doc.text("at 8 am")),
    ),
    estimations,
)
classs = sorted(classs)


"""
Example: ”Will it be mostly raining this weekend?”
"""
doc = Doc("Will it be mostly raining this weekend?")

weather_model = WeatherModel(doc.text("Directions from Monteray to San Francisco"))
weather = iter(weather_model)
weekend_weather = filter(
    weather_model.get_predicate(
        date_time=DateTime.resolve_from_document(doc=doc.text("this weekend"))
    ),
    weather,
)
weekend_weather = sorted(weekend_weather)

raining_weekend_weather = filter(
    weather_model.get_predicate(
        weather_condition=WeatherCondition.resolve_from_document(doc=doc.text("raining"))
    ),
    weather
)

mostly_raining = (len(list(raining_weekend_weather)) / len(list(weekend_weather))) > 0.5

command = DefaultResponseCommand(
    doc.text("Will it be mostly raining this weekend?")
)
#command.call(???)
