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
