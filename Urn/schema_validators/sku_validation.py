schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "parent_sku_guid": {
            "type": "string"
        },
        "category": {
            "type": "string"
        }
    },
    "required": ["name", "description"]
}
