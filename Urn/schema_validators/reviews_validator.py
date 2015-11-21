review_schema = {
    "type": "object",
    "properties": {
        "product_guid": {
            "type": "string"
        },
        "rating": {
            "type": "number"
        },
        "review_comment": {
            "type": "string"
        }
    },
    "required": ["product_guid", "rating", "review_comment"]
}

review_schema_put = {
    "type": "object",
    "properties": {
        "review_guid": {
            "type": "string"
        },
        "rating": {
            "type": "number"
        },
        "review_comment": {
            "type": "string"
        }
    },
    "required": ["review_guid"]
}

review_schema_delete = {
    "type": "object",
    "properties": {
        "review_guid": {
            "type": "string"
        }
    },
    "required": ["review_guid"]
}
