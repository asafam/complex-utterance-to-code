# App

## `App.resolve_from_text`

This API allows us to resolve an app or a website that will use to tp perform an action. For example, an app to send a message or create a reminder.

``` py
App.resolve_from_text(
    text: str
) : App
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual `App` description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `App`    | `App` object |

**Example**

A `App` can be a specific app like Gmail

{==

Reply back to Sue on Facebook saying I did not get the invite

==}

``` py
app = App.resolve_from_text("Facebook")
```
