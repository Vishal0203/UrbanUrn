schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "description": {
            "type": "string"
        },
        "business_image": {
            "type": "string"
        },
        "addresses": {
            "type": "array",
            "properties": {
                "street1": {"type": "string"},
                "street2": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "pincode": {"type": "string"},
                "country": {"type": "string"},
                "business": {"type": "object"}
            },
             "required": ["city", "pincode", "country"]
        },
    },
    "required": ["name", "addresses"]
}
