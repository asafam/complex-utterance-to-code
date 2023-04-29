# MessageContentType

## `MessageContentType.resolve_from_text`

This API allows us to resolve the message type that should be sent. Commonly we may find the textual decription for message content type like "audio" or "voice" .

It is possible that a user will specify a content type that should be interpreted as multiple content types. In that case, the API will return a list of `MessageContentType` objects.

``` py
MessageContentType.resolve_from_text(
    text: str
) : MessageContentType | List[MessageContentType]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual `MessageContentType` description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `MessageContentType | List[MessageContentType]`    | `MessageContentType` object or a list of `MessageContentType` objects based on the `text` parameter to this function. |

**Example**

Sending a voice message requires the `MessageContentType` to be resolved.

{==

Send a voice message to Ted

==}

``` py
message_content_type = MessageContentType.resolve_from_text("voice")
```
