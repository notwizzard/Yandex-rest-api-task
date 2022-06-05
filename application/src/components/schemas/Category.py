CATEGORY = {
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "type": { "type": "string", "enum": ["CATEGORY"] },
        "name": { "type": "string" },
        "parentId": { "type": ["string", "null"] }
    },
    "required": ["id", "type", "name", "parentId"] 
}