superuser_schema = {
    "type": "object",
    "properties": {
        "coupons": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string"
                    },
                    "discount_value": {
                        "type": "number"
                    },
                    "is_percentage": {
                        "type": "boolean"
                    }
                },
                "required": ["code", "discount_value", "is_percentage"]
            }
        }
    },
    "required": ["coupons"]
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
