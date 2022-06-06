from sqlite3 import connect
import psycopg2
from .databaseErrorList import ErrorList

class Database:

    def __init__(self):
        self.error = ErrorList.ok.value
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database="postgres",
                user="root",
                password="root",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()
        except:
            self.error = ErrorList.connection.value
            return False
        return True


    def get_data(self, params):
        pass


    def add_data(self, data):
        if not self.connect():
            return False

        units = [[d["id"], d["name"], d["type"], d["parentId"], data["updateDate"], d.get("price")] for d in data["items"]]
        args = [a for u in units for a in u]

        query = "INSERT INTO products (id, name, type, parentid, updatedate, price) VALUES "
        query += ",".join(["(%s, %s, %s, %s, %s, %s)"] * len(units))
        query += " ON CONFLICT (id) DO UPDATE SET (id, name, type, parentid, updatedate, price) = (EXCLUDED.id, EXCLUDED.name, EXCLUDED.type, EXCLUDED.parentid, EXCLUDED.updatedate, EXCLUDED.price)"

        try:
            self.cursor.execute(query, args)
            self.connection.commit()
        except:
            self.error = ErrorList.insertion.value
            return False
        finally:
            self.connection.close()

        return True
