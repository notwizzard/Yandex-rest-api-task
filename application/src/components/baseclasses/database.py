import psycopg2
from datetime import datetime
from .databaseErrorList import ErrorList
import queue

class Database:

    def __init__(self):
        self.error = ErrorList.ok.value
        self.connection = None
        self.cursor = None
        self.products_response = None
        self.statistics_response = None


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

    
    def execute(self, products_query, statistics_query, products_args, statistics_args):
        
        if not self.connect():
            return False

        try:
            if products_query != None:
                self.cursor.execute(products_query, products_args)
                try:
                    self.products_response = self.cursor.fetchall()
                except:
                    pass
            if statistics_query != None:
                self.cursor.execute(statistics_query, statistics_args)
                try:
                    self.statistics_response = self.cursor.fetchall()
                except:
                    pass
            self.connection.commit()
        except:
            self.error = ErrorList.execution.value
            return False
        finally:
            self.connection.close()

        return True


    def delete_data(self, id):

        products_query = "DELETE FROM products WHERE id=%s RETURNING id"
        statistics_query = "DELETE FROM statistics WHERE id=%s RETURNING id"

        if not self.execute(products_query, statistics_query, [id], [id]):
            return False

        if len(self.products_response) == 0:
            return False

        ids_to_delete = queue.Queue() 
        ids_to_delete.put(id)
        while not ids_to_delete.empty():
            products_query = "DELETE FROM products WHERE parentid=%s RETURNING id"
            statistics_query = "DELETE FROM statistics WHERE parentid=%s RETURNING id"

            next_id = ids_to_delete.get()
            if not self.execute(products_query, statistics_query, [next_id], [next_id]):
                return False
            
            if len(self.products_response) > 0:
                for i in self.products_response:
                    ids_to_delete.put(i)

        return True


    def import_data(self, data):

        units = [[d["id"], d["name"], d["type"], d["parentId"], data["updateDate"], d.get("price")] for d in data["items"]]
        args = [a for u in units for a in u]

        products_query = "INSERT INTO products (id, name, type, parentid, updatedate, price) VALUES "
        products_query += ",".join(["(%s, %s, %s, %s, %s, %s)"] * len(units)) 
        products_query += " ON CONFLICT (id) DO UPDATE SET (id, name, type, parentid, updatedate, price) = (EXCLUDED.id, EXCLUDED.name, EXCLUDED.type, EXCLUDED.parentid, EXCLUDED.updatedate, EXCLUDED.price)"

        statistics_query = "INSERT INTO statistics (id, name, type, parentid, updatedate, price) VALUES "
        statistics_query += ",".join(["(%s, %s, %s, %s, %s, %s)"] * len(units))

        if not self.execute(products_query, statistics_query, args, args):
            return False

        for item in data["items"]:
            if not self.update_date(item["parentId"], data["updateDate"]):
                return False
         
        return True

    
    def update_date(self, id, date):

        if id == None:
            return True

        query = "UPDATE products SET updatedate=%s WHERE id=%s RETURNING parentid"
        if not self.execute(query, None, [date, id], []):
            return False
        if len(self.products_response) > 0:
            return self.update_date(self.products_response[0], date)

        return True


    def get_nodes(self, id):
        root = self.get_tree_structure(id)        
        self.count_nodes_price(root)
    
        return root


    def count_nodes_price(self, root):
        if root == None:
            return

        if root["type"] == "OFFER":
            return root["price"], 1

        if root["type"] == "CATEGORY":
            total_price = 0
            total_number_of_offers = 0
            for child in root["children"]:
                t_p, t_n = self.count_nodes_price(child)
                total_price += t_p 
                total_number_of_offers += t_n
            
            total_number_of_offers = max(1, total_number_of_offers)
            root["price"] = total_price / total_number_of_offers

            return total_price, total_number_of_offers

    
    def get_tree_structure(self, id):

        query = "SELECT * FROM products WHERE id=%s"
        if not self.execute(query, None, [id], []):
            return None

        if len(self.products_response) == 0:
            return None 

        columns = ["type", "name", "id", "parentId", "date", "price"]
        root = self.response_to_object(self.products_response[0], columns)
        root["date"] = root["date"].isoformat() + "Z"
        root["children"] = None

        query = "SELECT id FROM products WHERE parentid=%s"
        if not self.execute(query, None, [id], []):
            return None

        children = self.products_response
        if len(children) > 0:
            root["children"] = []
        for child in children:
            root["children"].append(self.get_tree_structure(child))
        
        return root

    
    def response_to_object(self, response, columns):
        node = {}
        for i, col in enumerate(columns):
            node[col] = response[i]
        
        return node


    def create_node(self, data):
        return {
            "id": data["id"],
            "type": data["type"], 
            "name": data["name"],
        }
