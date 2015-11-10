wishlist_post = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        }
    },
    "required": ["product_guid"]
}

wishlist_delete = {
    "type": "object",
    "properties": {
        "wishlist_guid": {
            "type": "string"
        }
    },
    "required": ["wishlist_guid"]
}