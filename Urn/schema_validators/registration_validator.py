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
        "confirm_password": {
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
            "type": "string"
        },
        "email_notification": {
            "type": "string"
        },
        "sms_notification": {
            "type": "string"
        }
    },
    "required": ["email", "username", "password", "confirm_password", "first_name", "last_name", "phone"]
}
update_schema = {
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
            "type": "string"
        },
        "email_notification": {
            "type": "string"
        },
        "sms_notification": {
            "type": "string"
        }
    }
}

login_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string"
        },
        "password": {
            "type": "string"
        }
    },
    "required": ["username", "password"]
}
