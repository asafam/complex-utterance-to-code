# PlaceAttribute

## `PlaceAttribute.resolve_from_text`

This API allows us to resolve attributes of a place from a textual description. For example, whether a place is open or not including the openning hours of a place, or the stars review on it.

Potentially, this API may result in a list of `PlaceAttributes`

``` py
PlaceAttribute.resolve_from_text(
    text: str
) : PlaceAttribute | List[PlaceAttribute]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual `PlaceAttribute` description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `PlaceAttribute`    | `PlaceAttribute` object or a list of `PlaceAttribute` objects based on the `text` parameter to this function. |

**Example**

A `PlaceAttribute` can be a specific app like Gmail

{==

Order 2 packages organic creamy peanut butter from WholeFood.

==}

``` py
place_attribute = PlaceAttribute.resolve_from_text("open after midnight")
```
