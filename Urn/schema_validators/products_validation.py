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
        }
    },
    "required": ["name", "description", "sku_guid", "price", "product_data", "business_guid"]
}
