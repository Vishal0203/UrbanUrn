schema = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "discount_value": {
            "type": "number"
        },
        "is_percentage": {
            "type": "boolean"
        }
    },
    "required": ["product_guid", "discount_value", "is_percentage"]
}


put_schema = {
    "type": "object",
    "properties": {
        "discount_guid": {
            "type": "string"
        },
        "discount_value": {
            "type": "number"
        },
        "is_percentage": {
            "type": "boolean"
        }
    },
    "required": ["discount_guid"]
}
