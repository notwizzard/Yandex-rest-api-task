import pymongo
from .errorList import ErrorList

class Database:

    def __init__(self) -> None:
        self.error = ErrorList.ok.value
        self.client = self.connect()
        self.db = self.client.yandex_db
        self.products = self.db.get_collection('products')
        self.statistics = self.db.get_collection('statistics')


    def connect(self) -> pymongo.mongo_client.MongoClient:
        client = pymongo.MongoClient(
            host='localhost:27017',
            document_class=dict,
            tz_aware=False,
            connect=True)
        return client


    def delete_data(self, id):
        pass 


    def update_parent_date(self, item) -> None:
        parent_id = item['parentId']
        while parent_id:
            self.products.update_one({
                'id': parent_id
            }, {
                '$set': {
                    'date': item['date']
                }
            })
            
            parent_id = self.products.find_one({'id': parent_id})['parentId']


    def import_data(self, data) -> None:        
        
        def insert_item(item):
            self.products.insert_one(item)

        def update_item(item):
            old_item = self.products.find_one({'id': item['id']})
            self.products.update_one({
                'id': item['id']
            }, {
                '$set': item 
            })       
            self.update_parent_date(old_item)     

        data['items'].sort(key=lambda x: x['type'])

        for item in data['items']:
            item['date'] = data['updateDate']
            if item['type'] == 'CATEGORY':
                item['children'] = []
            else:
                item['children'] = None

            if self.products.find_one({'id': item['id']}):
                update_item(item)
            else:
                insert_item(item)

            self.update_parent_date(item)

    
    def build_node(self, root) -> tuple([int, int]):
            
        def set_price():
            root['price'] = total_price // max(1, number)

        root['date'] = root['date'].strftime("%Y-%m-%dT%H:%M:%SZ") 
        if root['type'] == 'OFFER':
            return root['price'], 1

        total_price = 0
        number = 0
        children = self.products.find({'parentId': root['id']}, {'_id': False})
        
        if not children:
            set_price()
            return total_price, number

        for child in children:
            p, n = self.build_node(child)
            root['children'].append(child)
            total_price += p
            number += n

        set_price()               

        return total_price, number


    def get_nodes(self, id) -> dict:

        root = self.products.find_one({'id': id}, {'_id': False})
        self.build_node(root)

        return root

