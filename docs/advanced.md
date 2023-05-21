# Advanced Topics

## Best practices and Convenient methods

Examples may show higher level of complexity. In this section we present best practices to implement the necessary code matching the phrase text.

This section also offers some utility methods that you can use in your code. We encourage you to use these methods to create a shorter code with better readability. These method wraps generic operations and include the boilercode to perform these operations.

### Size

Use the python `len()` function to return how many items are in the list.

!!! example

    {==

    If I have exactly one meeting on Friday send a message to mom saying that I will be free.

    ==}

    ``` py
    event_category = EventCategory.resolve_from_text("meeting")
    date_time = DateTime.resolve_from_text("on Friday")
    events = Event.find_events(
        event_category=event_category,
        date_time=date_time
    )
    expr = len(events) == 1

    if expr:
        recipient = Contact.resolve_from_text("mom")
        content = Content.resolve_from_text("I will be free")
        Message.send_message(
            recipient=recipient,
            content=content
        )
    ```

Oftentimes, we will use the `len()` function to verify a certain condition expression is true.

!!! example

    {==

    If I didn't get any message from Louie yesterday text him to call me.

    ==}

    ``` py
    sender = Contact.resolve_from_text("Louie")
    date_time = DateTime.resolve_from_text("yesterday")
    messages = Messages.find_messages(
        sender=sender,
        date_time=date_time
    )
    expr = len(messages) == 0

    if expr:
        recipient = sender
        content = Content.resolve_from_text("call me")
        Message.send_message(
            recipient=recipient,
            content=content
        )
    ```

### First / last `N` elements

We provide a convenient method to return the first (or last) `N` elements (defaults to 1 if not specified).

Prefer using this method over Pyton slicing, if you are familiar with it.

    ```py
    utils.first(items: List[Entity], n: int): List[Entity]
    ```

Parameters:

    items: `List[Entity]`
        A list of items.

    n: `int`
        Number of items to fetch in the list.

!!! example

    {==

    Delete the last 2 messages from Henry.

    ==}

    ``` py
    sender = Contact.resolve_from_text("Henry")
    messages = Messages.get_message(sender=sender)
    messages = utils.last(messages, 2)
    Message.delete_messages(messages=messages)
    ```

### All

Return whether every element is True or equivalent (e.g. non-zero or non-empty).

Returns False in case there is at least one element within a series or along a Dataframe axis that is True or equivalent.

    ```py
    utils.all(items: List[Entity], **kwargs)
    ```

Parameters:

    items: `List[Entity]`
        A list to perform the test on.

    **kwargs:
        Arguments list according to the action API `find_` function arguments.

!!! example

    {==

    Will it rain every day this weekend?

    ==}

    ``` py
    # find the weather forecasts for every day this weekend
    date_time = DateTime.resolve_from_text("this weekend")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time
    )
    # arguments to test for all items in the list
    weather_attr = WeatherAttribute.resolve_from_text("rain")
    utils.all(weather_forecasts, weather_attr=weather_attr)
    ```

### `sort`

Sort by a specific type.

!!! example

    {==

    Get directions to the nearest pharmacy.

    ==}

    ```py
    destinations = Location.resolve_from_text("pharmacy")
    destinations = utils.sort(destinations, "nearest")
    destination = utils.first(destinations)
    navigation_directions = Navigation.find_directions(
        destination=destination
    )
    Responder.respond(response=navigation_directions)
    ```

### `most`

Return True whether the majority of items in a list are matching a given criteria.

    ```py
    utils.most(items: List[Entity], **kwargs): List[Entity]
    ```

Parameters:

    items: `List[Entity]`
        A list of items.

    **kwargs:
        Arguments list according to the action API `find_` function arguments.

!!! example

    {==

    Is it going to be mostly rainy over this weekend?

    ==}

    ``` py
    weather_attribute = WeatherAttribute.resolve_from_text("rainy")
    date_time = DateTime.resolve_from_text("this weekend")
    weather_forecasts = Weather.find_weather_forecasts(
        date_time=date_time
    )
    result = utils.most(
        weather_forecasts,
        weather_attribute=weather_attribute
    )
    Responder.respond(response=result)
    ```

### `filter`

Some user requests will require additional filtering on the actions results.

This method subsets the data according to specified data types resolved from the text.

    ```py
    utils.filter(items: List[Entity], **kwargs): List[Entity]
    ```

Parameters:

    items: `List[Entity]`
        A list of items.

     **kwargs:
        Arguments list according to the action API `find_` function arguments.

!!! example

    {==

If the road to my office is icy then text John to expect traffic.

    ==}

    ```py
    destination = Location.resolve_from_text("my office")
    nav_road_conditions = NavigationRoadConditions.resolve_from_text("icy")
    navigation_directions = Navigation.find_directions(
        destination=destination,
        nav_road_conditions=nav_road_conditions
    )
    expr = len(navigation_directions) > 0

    if expr:
        recipient = Contact.resolve_from_text("John")
        content = Content.resolve_from_text("expect traffic")
        Message.send_message(
            recipient=recipient,
            content=content
        )
    ```

We first query for directions to a specific destination ("the office") and show it to the user.

Then, we need to filter the results for any matches to the requested criteria (in this example: road conditions are "icy").

### `map`

This method applies a function returns a value to every item of a list according to a textual description.

The `map` function is usually used to extract values on a fetched list of items.

    ```py
    utils.map(items: List[Entity], text: str): List[Entity]
    ```

Parameters:

    items: `List[Entity]`
        A list of items.

    text: `str`
        Text value to map the list items according to.

!!! example

    {==

    Email all attendees on the 9am meeting that I am running late.

    ==}

    ```py
    date_time = DateTime.resolve_from_text("9am")
    events = Event.find_events(date_time=date_time)
    recipients = utils.map(events, "all attendees")
    for recipient in recipients:
        content = Content.resolve_from_text("I am running late")
        Message.send_message(
            recipient=recipient,
            content=content
        )
    ```

## Exceptions and errors

Sometimes users make requests that cannot be fulfilled, like when requesting for a non existant date (Feb 30th) or when one of the requests should not produce any results ("Delete all emails from Gavin" where Gavin never sent an email).

When writing code, you can assume no failures should happen due to the user provided inputs and call the APIs without worrying for any exceptions.

The system deals with such failures and operates a recovery mechanism. The recovery mechanism tries to recover from all these exceptions by describing the problem to the user and prompting a corrected input or dismissal of the user utterance. **This is out of scope of this work and you should not bother youself with details about it**
