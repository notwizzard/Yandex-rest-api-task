from .request import Request
from datetime import datetime
from .requestErrorList import ErrorList

class ImportRequest(Request):
    def __init__(self, request):
        super().__init__(request)
    
    def validate(self, schema):
        if not super().validate(schema):
            return False
        
        try:
            self.data["updateDate"] = datetime.fromisoformat(self.data["updateDate"])
        except:
            self.error = ErrorList.validation.value
            return False
        return True