SHOP_UNIT_IMPORT_REQUEST = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": { 
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
        },
        "updateDate": { "type": "string" }
    },
    "required": ["items", "updateDate"]    
}