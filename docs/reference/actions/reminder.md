# Reminder

## `Reminder.find_reminders`

This API provides us the reminders in our mobile device.

``` py
Reminder.find_reminders(
    date_time: Optional[DateTime],
    person_reminded: Optional[Contact],
    content: Optional[Content],
    app: Optional[Resurce]
) : List[ReminderEntity]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `date_time`        | `DateTime`  | Yes        | Date and time the reminder was recieved        |
| `person_reminded`        | `Contact`  | Yes        | Reminder contact reminded        |
| `content`        | `Content`  | Yes        | Content within the reminder        |
| `app`        | `App`  | Yes        | The reminder app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[ReminderEntity]`    | List of `ReminderEntity` objects |

**Example**

{==

What reminders do I have on next friday?

==}

``` py
contact = Contact.resolve_from_text("I")
person_reminded = contact
date_time = DateTime.resolve_from_text("on next friday")
reminders = Reminder.find_reminders(
    sender=sender,
    date_time=date_time
)
response = reminders
Responder.respond(response=response)
```

## `Reminder.create_reminder`

This API provides us the functionality of creating a reminder.

``` py
Reminder.create_reminder(
    date_time: Optional[DateTime],
    person_reminded: Optional[Contact],
    content: Optional[Content],
    app: Optional[Resurce]
) : ReminderEntity
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `date_time`        | `DateTime`  | Yes        | Date and time the reminder was recieved        |
| `person_reminded`        | `Contact`  | Yes        | Reminder contact reminded        |
| `content`        | `Content`  | Yes        | Content within the reminder        |
| `app`        | `App`  | Yes        | The reminder app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `ReminderEntity`    | The reminder object that was created |

**Example**

{==

Remind dance troupe to bring extra socks to practice.

==}

``` py
contact = Contact.resolve_from_text("dance troupe")
person_reminded = contact
content = Content.resolve_from_text("bring extra socks to practice.")
reminders = Reminder.create_reminder(
    person_reminded=person_reminded,
    content=content
)
```

## `Reminder.update_reminder`

This API provides us the functionality of updating a reminder.

``` py
Reminder.update_reminder(
    date_time: Optional[DateTime],
    new_date_time: Optional[DateTime],
    person_reminded: Optional[Contact],
    new_person_reminded: Optional[Contact],
    content: Optional[Content],
    new_content: Optional[Content],
    app: Optional[Resurce],
    new_app: Optional[Resurce]
) : ReminderEntity
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `date_time`        | `DateTime`  | Yes        | Date and time the reminder was recieved        |
| `new_date_time`        | `DateTime`  | Yes        | New date and time the reminder was recieved        |
| `person_reminded`        | `Contact`  | Yes        | Reminder contact reminded        |
| `new_person_reminded`        | `Contact`  | Yes        | Reminder to a new contact reminded        |
| `content`        | `Content`  | Yes        | Content within the reminder        |
| `new_content`        | `Content`  | Yes        | New content within the reminder        |
| `app`        | `App`  | Yes        | The reminder app application |
| `new_app`        | `App`  | Yes        | A new reminder app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `ReminderEntity`    | The reminder object that was updated |

**Example**

{==

Change my reminder for the doctor's appointment at 11am to 10am

==}

``` py
contact = Contact.resolve_from_text("Stephanie")
contactt_reminded = contact
content = Content.resolve_from_text("the doctor's appointment")
date_time = DateTime.resolve_from_text("at 11am")
new_date_time = DateTime.resolve_from_text("10am")
reminders = Reminder.reply_reminder(
    contactt_reminded=contactt_reminded,
    content=content,
    date_time=date_time,
    new_date_time=new_date_time
)
```

## `Reminder.delete_reminders`

This API provides us the functionality to delete specific reminder or a group of reminders.

``` py
Reminder.reply_reminders(
    reminder: ReminderEntity|List[ReminderEntity]
) : None
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `reminders`        | `ReminderEntity|List[ReminderEntity]`  | No        | A specific reminder to delete or an iterable that upon iteration - deletes every reminder       |

**Returns**

This function does not return.

**Example**

{==

Cancel the reminder on the 31st that the library summer reading program shop closes.

==}

``` py
content = Content.resolve_from_text("the library summer reading program shop closes")
date_time = DateTime.resolve_from_text("on the 31st")
reminders = Reminder.find_reminders(
    content=content,
    date_time=date_time
)
Reminder.delete_reminders(reminders=reminders)
```
