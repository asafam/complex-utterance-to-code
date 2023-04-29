# Getting started

Let's learn by example.

Throughout this tutorial, we’ll walk you through the creation of a basic Python code for given virtual agent user commands.

We collected user commands for a virtual assistance (like Siri or Alexa). The virtual assistant offers help in navigation, weather forecasts, messaging, reminders, shopping and more. The goal of this project is to match user commands in English to a valid Python code.

We’ll assume you have a basic experience with Python already.

## Simple commands

Simple commands express a single action that the virtual assistant is expected to perform.

### Simple command example

Let's start by writing a code for a simple user command:

{==

Get directions from Disneyland to my house.

==}

To match this user command we need to map it with the `Navigation.find_directions(origin: Optional[Location], destination: Location)` function in the [Navigation] API.

[navigation]: reference/actions/navigation.md

```py
origin = Location.resolve_from_text("Disneyland")
destination = Location.resolve_from_text("my house")
navigation_directions = Navigation.find_directions(
    origin=origin,
    destination=destination
)
Responder.respond(response=navigation_directions)
```

`Navigation.find_directions` is taking an origin `Location` and a destination `Location` as its parameters.

We first create the origin `Location` object. We name it according to the argument name `origin`. A text is usually mapped to a variable using the `resolve_from_text()` function.

Likewise, we then create the destination `Location` object and name it with the argument name `destination`.

Next, we plug the `origin` and `destination` parameters into the `Navigation.find_directions` function call. This function will return a list of navigation directions.

Last, we report back the result to the user using the `Responder.respond(response: Entity|List[Entity])` API. As the `response` we set the `navigation_directions` result from the previous step.

### Another simple command example

Another simple user command:

{==

Text Karen that I will be late.

==}

To match this user command we need to map it with the `Messages.send_message(recipient: Contact, content: Content)` API in the [Messaging] API.

[messaging]: reference/actions/message.md

```py
recipient = Contact.resolve_from_text("Karen")
content = Content.resolve_from_text("I will be late")
Messages.send_message(
    recipient=recipient,
    content=content
)
```

We first create the `Contact` object and name it according to the argument name `recipient`.

Similarly, we create the `Content` object and name it `content`.

Next, we plug the `recipient` and `content` parameters into the `Messages.send_message` function call to call the function with its arguments.

## Complex commands

Complex commands can express multiple simple commands together like in sequences or conditions. Alterntaively, complex can call a simple commands multiple times like in loops.

Let's see some examples for complex commands.

### Complex command example

Complex user command:

{==

Get directions from Disneyland to my house and text them to Robert.

==}

We already went over the first part of the command ("Get directions from Disneyland to my house").

```py
origin = Location.resolve_from_text("Disneyland")
detination = Location.resolve_from_text("my house")
navigation_directions = Navigation.find_directions(
    origin=origin,
    destination=destination
)
```

Let's see the other part and put the code together. To match "text them to Robert" user command we need to map it with the `Messages.send_message` API.

```py
recipient = Contact.resolve_from_text("Robert")
content = Content.resolve_from_entity(navigation_directions)
Messages.send_message(
    recipient=recipient,
    content=content
)
```

We create the `Contact` object and name it `recipient`.

Now we need to create the `Content` object. Notice that in this example, the content of the message in this example is the navigation directions list we got on the previous step. Therefore, we use the utility function `Content.resolve_from_entity()` to cast the `navigation_direction` entity to a `Content` entity.

Last, we call the `Messages.send_message` function with its arguments.

The final code should look like this:

```py
origin = Location.resolve_from_text("Disneyland")
destination = Location.resolve_from_text("my house")
navigation_direction = Navigation.find_directions(
    origin=origin,
    destination=destination
)

recipient = Location.resolve_from_text("Robert")
content = Content.resolve_from_entity(navigation_direction)
message = Messages.send_message(
    recipient=recipient,
    content=content
)
```

### Another complex command example

Let's see another complex user command:

{==

Remind me to bring an umbrella if it rains tomorrow.

==}

The first part of the command: "Remind me to bring an umbrella" is conditioned by the second part of the sentence "if it rains tomorrow".

Conditions are another building blocks of complex commands.

First, we get the weather forecasts by using the `Weather.find_weather_forecasts(date_time: Optional[DateTime], weather_attribute: Optional[WeatherAttribute])` in the [Weather] API.

[weather]: reference/actions/weather.md

```py
date_time = DateTime.resolve_from_text("tomorrow")
weather_attribute = WeatherAttribute.resolve_from_text("rains")
weather_forecasts = Weather.find_weather_forecasts(
    date_time=date_time,
    weather_attribute=weather_attribute
)
```

!!! note
This API takes additional optional arguments, like a location, which we did not include in this example. In that case, the API assumes default values for the unspecified arguments (like the current location). Don't bother yourself with it and use only what is specified in the example.

Then, we check for the truthness of the condition expression. It will be valid if the `Weather.find_weather_forecasts` returned any result. This function return a list of weather forecases that match the `DateTime` and `WeatherAttribute`.

```py
expr = len(list(weather_forecasts)) > 0
if expr:
```

The condition body should include the "Remind me to bring an umbrella" command.

```py
person_reminded = Contact.resolve_from_text("me")
content = Content.resolve_from_text("Bring an umbrella").
Reminder.create_reminder(
    person_reminded=person_reminded,
    content=content
)
```

We follow the `Reminder.create_reminder(person_reminded: Optional[Contact], content: Content)` API spec.

!!! note
Notice that in the `content` object we omit the word "to" and keep the content that should appear in the reminder ("bring an umbrella").

Putting everything together:

```py
date_time = DateTime.resolve_from_text("tomorrow")
weather_attribute = WeatherAttribute.resolve_from_text("rains")
weather_forecasts = Weather.find_weather_forecasts(
    date_time=date_time,
    weather_attribute=weather_attribute
)
expr = len(weather_forecasts) > 0
if expr:
    person_reminded = Contact.resolve_from_text("me")
    content = Content.resolve_from_text("bring an umbrella")
    reminder = Reminders.create_reminder(
        person_reminded=person_reminded,
        content=content
    )
```

### Yet another complex command example

Let's see one more complex user command:

{==

What is the weather in Paris and London?

==}

We will execute this command in a loop iterating over "Paris" and "London", althought it can be executed it in a sequence like previous commands.

Weather forecasts are returned in the `Weather.find_weather_forecasts(location: Optional[Location])`

We are required to report back to the user every result. This is done using `Responder.respond(response: Entity | List[Entity])`. Since we are looping, we collect all responses in the response `list` and pass it to the `Responder.respond()` function.

```py
location1 = Location.resolve_from_text("Paris")
location2 = Location.resolve_from_text("London")
response = []
for location in [location1, location2]:
    weather_forecasts = Weather.find_weather_forecasts(location=location)
    response.append(weather_forecasts)
Responder.respond(response=response)
```

### Last complex command example

We'll finish this part of the tutorial with one last complex user command:

{==

Show me the traffic to each Whole Food branch in a 10 miles radius.

==}

Traffic information is acquired using the `Navigation.find_traffic_info(destination: Optional[Location])` API in the [Navigation] API.

```py
destinations = Location.resolve_many_from_text("each Whole Food branch")
destinations = utils.filter()
response = []
for destination in destinations:
    traffic_info = Navigation.find_traffic_info(destination=destination)
    if traffic_info:
        response.append(traffic_info)
Responder.respond(response=response)
```

While in previous examples we saw specific location names (e.g. Disneyland, my house), in this example we are looking at a group of locations. The function `Location.resolve_many_from_text` should be used to return a list of `Location` objects (like in this case) according to the text argument it is called with.

We get a list of `Location` using `Location.resolve_from_text`. The full text describing the location should be provided to it: `each Whole Food branch in a 10 miles radius`.

Next, we loop over the list of `Location` from the previous step and find the Navigation traffic information using the `Navigation.find_traffic_info()`.

We append each traffic info result to a `response` list and when the loop finishes we call the `Responder.respose()` with this list.
