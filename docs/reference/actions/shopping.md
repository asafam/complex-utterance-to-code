# Shopping

Shopping

## `Shopping.find_stores`

This API allows us to find stores according to specific criteria, like the products sold in these stores, or when these stores are open.

```py
Shopping.find_stores(
    date_time: Optional[DateTime],
    location: Optional[Location],
    product: Optional[Product],
    place_attribute: Optional[PlaceAttribute],
) : List[StoreEntity]
```

**Arguments**

| Name         | Type               | Optional | Description                                                                          |
| ------------ | ------------------ | -------- | ------------------------------------------------------------------------------------ |
| `date_time`  | `DateTime`         | Yes      | Date and time of the event                                                           |
| `location`   | `Location`         | Yes      | Location of the store                                                                |
| `product`    | `CommerceCategory` | Yes      | The product sold bt the store                                                        |
| `place_attr` | `PlaceAttribtue`   | Yes      | Attributes of the store. For example, is it close or open, ratings, peak hours, etc. |

**Returns**

| Type                | Description                   |
| ------------------- | ----------------------------- |
| `List[StoreEntity]` | List of `StoreEntity` objects |

**Example**

{==

Find all open stores near my office that sell discounted Skippy peanut butter.

==}

```py
place_attribute = PlaceAttribute.resolve_from_text("open")
location = Location.resolve_from_text("near my office")
product_name = ProductName.resolve_from_text("discounted Skippy peanut butter")
stores = Shopping.find_stores(
    place_attribute=place_attribute,
    location=location,
    product_name=product
)
Responder.respond(response=stores)
```
