# NavTravelMethod

## `NavTravelMethod.resolve_from_text`

This API allows us to resolve a navigation method for travelling. Driving a car or riding a bicycle are both method of travel that can appear in a user command.

``` py
NavTravelMethod.resolve_from_text(
    text: str
) : NavTravelMethod | List[NavTravelMethod]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual navigation travelling method description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `NavTravelMethod`    | `NavTravelMethod` object |

**Example**

{==

how long is the road to SF on the PCH riding a bicycle

==}

``` py
nav_travel_method = NavTravelMethod.resolve_from_text("riding a bicycle")
```
