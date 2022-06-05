from .request import Request

class ImportRequest(Request):
    def __init__(self, request):
        super().__init__(request)
    
    def validate(self, schema):
        return super().validate(schema)