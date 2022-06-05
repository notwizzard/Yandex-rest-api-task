import enum

class ErrorList(enum.Enum):
    ok = {
        "code": 200
    }
    validation = {
        "code": 400,
        "message": "Validation Failed"
    }