schema = {
    "type": "object",
    "properties": {
        "street1": {
            "type": "string"
        },
        "street2": {
            "type": "string"
        },
        "city": {
            "type": "string"
        },
        "state": {
            "type": "string"
        },
        "pincode": {
            "type": "string"
        },
        "country": {
            "type": "string"
        }
    },
    "required": ["city", "pincode", "country"]
}