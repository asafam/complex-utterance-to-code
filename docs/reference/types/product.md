# Product

## `Product.resolve_from_text`

This API allows us to resolve a product from a text. A product is not limited to the product category but can also include the product brand and manufacturer, For example, the text "car insurance", "iPhone 14", "Detroit deep dish pizza" or "polka dot black dress" should all be reolved in this API.

It is possible that given a specific `text` input this API will infer it as a list of `Product` objects. For example, "all The Hobbit trilogy books" should results in a list of `Product` objects for each book in the bespoken trilogy.

``` py
Product.resolve_from_text(
    text: str
) : Product | List[Product]
```

**Arguments**

| Name          | Type          | Optional  | Description                              |
| ------------- | --------------| --------- | ---------------------------------------- |
| `text`        | `str`         | No        | Textual `Product` description        |

**Returns**

| Type          | Description       |
| ------------- | ----------------- |
| `Product | List[Product]`    | `Product` object or a list of `Product` objects based on the `text` parameter to this function. |

**Example**

A `Product` can be include the product's brand, vendor, name and different features. Please note the price cmparison should be achieved using the `min` utility functions (see more in the Advanced Topics section).

{==

Where can I find a store cheapest price for the new Lego knights castle that has it in stock?

==}

``` py
product = Product.resolve_from_text("the new Lego knights castle")
```
