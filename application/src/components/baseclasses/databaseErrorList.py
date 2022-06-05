import enum

class ErrorList(enum.Enum):
    ok = "ok"
    insertion = "Insertion Failed"
    selection = "Selection Failed"
    connection = "Connection Failed"
