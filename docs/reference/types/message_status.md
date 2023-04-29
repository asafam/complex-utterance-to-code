# MessageStatus

## `MessageStatus.resolve_from_text`

This API allows us to resolve a message status from a user query. Statuses like "new", "unread" or "seen" for messages are common to be found and should be resolved. 

Take note that the return value from this function can be a list of `MessageStatus` objects, like in the case where the user command ask "any message status".

``` py
MessageStatus.resolve_from_text(
    text: str
) : MessageStatus | List[MessageStatus]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual `MessageStatus` description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `MessageStatus | List[MessageStatus]`    | `MessageStatus` object or a list of `MessageStatus` objects based on the `text` parameter to this function. |

**Example**

A `MessageStatus` denote the message status "read" in a user command:

{==

Delete every seen message from Google to me.

==}

``` py
message_status = MessageStatus.resolve_from_text("seen")
```
