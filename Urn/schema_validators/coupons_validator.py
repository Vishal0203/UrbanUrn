superuser_schema = {
    "type": "object",
    "properties": {
        "code": {
            "type": "string"
        },
        "discount_value": {
            "type": "number"
        },
        "is_percentage": {
            "type": "string"
        }
    },
    "required": ["code", "discount_value", "is_percentage"]
}


general_schema = {
    "type": "object",
    "properties": {
        "code": {
            "type": "string"
        }
    },
    "required": ["code"]
}
