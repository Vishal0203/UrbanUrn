schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string"
        },
        "username": {
            "type": "string"
        },
        "password": {
            "type": "string"
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "phone": {
            "type": "string"
        },
        "push_notification": {
            "type": "boolean"
        },
        "email_notification": {
            "type": "boolean"
        },
        "sms_notification": {
            "type": "boolean"
        }
    },
    "required": ["email", "username", "password", "first_name", "last_name", "phone"]
}
