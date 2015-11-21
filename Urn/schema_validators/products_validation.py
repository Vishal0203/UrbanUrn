schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "price": {
            "type": "number"
        },
        "product_data": {
            "type": "string"
        },
        "sku_guid": {
            "type": "string"
        },
        "business_guid": {
            "type": "string"
        },
        "is_fragile": {
            "type": "boolean"
        }
    },
    "required": ["name", "description", "sku_guid", "price", "product_data", "business_guid"]
}


put_schema = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "sku_guid": {
            "type": "string"
        }
    },
    "required": ["product_guid", "sku_guid"]
}
