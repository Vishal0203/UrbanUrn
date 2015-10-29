post_auth_schema = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "user_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        }
    },
    "required": ["product_guid", "user_guid", "product_data"]
}

post_non_auth_schema = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        }
    },
    "required": ["product_guid", "product_data"]
}

put_auth_schema = {
    "type": "object",
    "properties": {
        "cart_item_guid": {
            "type": "string"
        },
        "product_guid": {
            "type": "string"
        },
        "user_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        }
    },
    "required": ["cart_item_guid", "product_guid", "user_guid", "product_data"]
}

put_non_auth_schema = {
    "type": "object",
    "properties": {
        "cart_item_guid": {
            "type": "string"
        },
        "product_guid": {
            "type": "string"
        },
        "product_data": {
            "type": "string"
        }
    },
    "required": ["cart_item_guid", "product_guid", "product_data"]
}

delete_auth_schema = {
    "type": "object",
    "properties": {
        "cart_item_guid": {
            "type": "string"
        },
        "user_guid": {
            "type": "string"
        }
    },
    "required": ["cart_item_guid", "user_guid"]
}


delete_non_auth_schema = {
    "type": "object",
    "properties": {
        "cart_item_guid": {
            "type": "string"
        }
    },
    "required": ["cart_item_guid"]
}
