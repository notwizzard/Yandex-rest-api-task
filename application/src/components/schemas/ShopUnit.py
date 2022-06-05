SHOP_UNIT = {
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "type": { "type": "string", "enum": ["OFFER", "CATEGORY"] },
        "name": { "type": "string" },
        "parentId": { "type": ["string", "null"] },
        "price": { "type": "number" }
    },
    "required": ["id", "type", "name", "parentId"] 
}