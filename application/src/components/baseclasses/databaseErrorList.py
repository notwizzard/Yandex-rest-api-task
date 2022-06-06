import enum

class ErrorList(enum.Enum):
    ok = "ok"
    execution = "Execute Failed"
    connection = "Connection Failed"
