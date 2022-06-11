import enum

class ErrorList(enum.Enum):
    ok = {
        "code": 200
    }
    validation = {
        "code": 400,
        "message": "Validation Failed"
    }
    existence = {
        "code": 404,
        "message": "Item not found"
    }
    runtime = {
        "code": 500,
        "message": "Server error"
    }
