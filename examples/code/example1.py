destination = Location.resolve_from_text("New Robert")
date_time = DateTime.resolve_from_text("5 AM")
duration = Navigation.find_duration(destination=destination, date_time=date_time)
Responder.respond(response=duration)

if [destination]:
    data = [x for x in data if x.destination == destination]
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("bring a coat")
    Reminder.create_reminder(person_reminded=person_reminded, content=content)
