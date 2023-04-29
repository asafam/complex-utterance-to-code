# Message

Messages can be emails or direct message apps (like Whatsapp). By default, the API will assume emails are requested. In cast another app shuld be used, the API provides the `app` parameter to serve that.

## `Message.find_messages`

This API provides us the messages in our mobile device.

``` py
Message.find_messages(
    date_time: Optional[DateTime],
    sender: Optional[Contact],
    recipient: Optional[Contact],
    content: Optional[Content],
    message_status: Optional[MessageStatus],
    message_content_type: Optional[MessageContentType],
    app: Optional[App]
) : List[MessageEntity]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `date_time`        | `DateTime`  | Yes        | Date and time the message was recieved        |
| `sender`        | `Contact`  | Yes        | Message sender        |
| `recipient`        | `Contact`  | Yes        | Message recipient        |
| `content`        | `Content`  | Yes        | Content within the message        |
| `message_status`        | `MessageStatus`  | Yes        | The message status. For example, "unread" or "new" |
| `message_content_type`        | `MessageContentType`  | Yes        | The message content type |
| `app`        | `App`  | Yes        | The message app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `List[MessageEntity]`    | List of `MessageEntity` objects |

**Example**

{==

Read the last unread message from aunt Bessy

==}

``` py
sender = Contact.resolve_from_text("aunt Bessy")
message_status = MessageStatus.resolve_from_text("unread")
messages = Message.find_messages(
    sender=sender,
    message_status=message_status
)
message = utils.last(messages)
Responder.respond(response=message)
```

## `Message.send_message`

This API provides us the functionality of sending a message.

``` py
Message.send_message(
    recipient: Optional[Contact],
    content: Optional[Content],
    message_content_type: Optional[MessageContentType],
    app: Optional[Resurce]
) : MessageEntity
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `recipient`        | `Contact`  | Yes        | Message recipient        |
| `content`        | `Content`  | Yes        | Content within the message        |
| `message_content_type`        | `MessageContentType`  | Yes        | The message content type |
| `app`        | `App`  | Yes        | The message app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `MessageEntity`    | The message object that was sent |

**Example**

{==

Record a voice message for Daryl

==}

``` py
contact = Contact.resolve_from_text("Daryl")
sender = contact
message_content_type = MessageContentType.resolve_from_text("voice")
messages = Message.send_message(
    sender=sender,
    message_content_type=message_content_type
)
```

## `Message.reply_message`

This API provides us the functionality of replying to a message, when the user explicitly states a reply action.

``` py
Message.reply_message(
    recipient: Optional[Contact],
    content: Optional[Content],
    message_content_type: Optional[MessageContentType],
    app: Optional[Resurce]
) : MessageEntity
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `recipient`        | `Contact`  | Yes        | Message recipient        |
| `content`        | `Content`  | Yes        | Content within the message        |
| `message_content_type`        | `MessageContentType`  | Yes        | The message content type |
| `app`        | `App`  | Yes        | The message app application |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `MessageEntity`    | The message object that was sent |

**Example**

{==

Reply with a voice message to Stephanie on Whatsapp

==}

``` py
contact = Contact.resolve_from_text("Stephanie")
sender = contact
message_content_type = MessageContentType.resolve_from_text("voice")
app = App.resolve_from_text("Whatsapp")
messages = Message.reply_message(
    sender=sender,
    message_content_type=message_content_type,
    app=app
)
```

## `Message.delete_messages`

This API provides us the functionality to delete a specific message or a group of messages.

``` py
Message.delete_messages(
    messages: MessageEntity|List[MessageEntity]
) : None
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `messages`        | `MessageEntity|List[MessageEntity]`  | No        | A specific message or a list of messages to delete      |

**Returns**

This function does not return.

**Example**

{==

Delete the last 2 messages

==}

``` py
messages = Message.find_messages()
messages = utils.last(messages, 2)
Message.delete_messages(messages=messages)
```

## `Message.archive_messages`

This API provides us the functionality to archive a specific message or a group of messages.

``` py
Message.archive_messages(
    messages: MessageEntity|List[MessageEntity]
) : None
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `messages`        | `MessageEntity|List[MessageEntity]`  | No        | A specific message or a list of messages to archive      |

**Returns**

This function does not return.

**Example**

{==

Archive the messages that are marked as read from Debby.

==}

``` py
sender = Contact.resolve_from_entity("Debby")
message_status = MessageStatus.resolve_from_text("marked as read")
messages = Message.find_messages(
    sender=sender,
    message_status=message_status
)
Message.archive_messages(messages=messages)
```
