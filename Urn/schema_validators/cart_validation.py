post_schema = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        },
        "wishlist_guids": {
            "type": "array"
        }
    }
}

put_schema = {
    "type": "object",
    "properties": {
        "cart_item_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        }
    },
    "required": ["cart_item_guid", "product_data"]
}

delete_schema = {
    "type": "object",
    "properties": {
        "cart_item_guid": {
            "type": "string"
        }
    },
    "required": ["cart_item_guid"]
}
