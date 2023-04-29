# NavRoadCondition

## `NavRoadCondition.resolve_from_text`

This API allows us to resolve a road condition out of navigation related queries.

``` py
NavRoadCondition.resolve_from_text(
    text: str
) : NavRoadCondition | List[NavRoadCondition]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual NavRoadCondition description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `NavRoadCondition | List[NavRoadCondition]`    | `NavRoadCondition` object or a list of `NavRoadCondition` objects based on the `text` parameter to this function. |

**Example**

{==

Get directions to downtown Detroit without flooding

==}

``` py
nav_road_condition = NavRoadCondition.resolve_from_text("flooding")
```
