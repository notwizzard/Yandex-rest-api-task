import jsonschema
from jsonschema import validate
from .errorList import ErrorList

class Request:

    def __init__(self, request):
        self.data = request
        self.error = ErrorList.ok.value

    def validate(self, schema):
        try:
            validate(self.data, schema)
        except jsonschema.exceptions.ValidationError:
            self.error = ErrorList.validation.value
            return False
        return True
