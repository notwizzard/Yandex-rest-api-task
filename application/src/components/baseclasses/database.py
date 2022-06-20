from typing import Dict, List, Tuple
from datetime import datetime
import pymongo
from .errorList import ErrorList

class Database:

    def __init__(self) -> None:
        self.error = ErrorList.ok.value
        self.client = self.connect()
        self.db = self.client.yandex_db
        self.products = self.db.get_collection('products')
        # self.sales = self.db.get_collection('sales')
        # self.statistics = self.db.get_collection('statistics')


    def connect(self) -> pymongo.mongo_client.MongoClient:
        client = pymongo.MongoClient(
            host='localhost:27017',
            document_class=dict,
            tz_aware=False,
            connect=True)
        return client


    def delete_data(self, item_id : str) -> bool:
        
        def delete_item(id: str) -> None:
            self.products.delete_one({'id': id})

        def delete_tree(id: str) -> None:
            children = self.products.find({'parentId': id})
            if not children:
                return delete_item(id)

            for child in children:
                delete_tree(child['id'])

            return delete_item(id)

        item = self.products.find_one({'id': item_id})
        if not item:
            return False

        delete_tree(item_id)

        return True


    def update_parent_date(self, item : Dict) -> None:

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


    def import_data(self, data : Dict) -> None:        
        
        def insert_item(item : Dict) -> None:
            self.products.insert_one(item)

        def update_item(item : Dict, old_item : Dict) -> None:
            self.products.update_one({
                'id': item['id']
            }, {
                '$set': item 
            })  

            if old_item['parentId'] != item['parentId']:
                self.update_parent_date(old_item)
                self.update_parent_date(item)
                return

            if old_item.get('price') != item.get('price'):
                self.update_parent_date(item)
                     
        data['items'].sort(key=lambda x: x['type'])

        for item in data['items']:
            item['date'] = data['updateDate']
            if item['type'] == 'CATEGORY':
                item['children'] = []
            else:
                item['children'] = None

            old_item = self.products.find_one({'id': item['id']})
            if old_item:
                update_item(item, old_item)
            else:
                insert_item(item)

            self.update_parent_date(item)

    
    def build_node(self, root : Dict) -> Tuple[int, int]:
        
        def set_price():
            root['price'] = total_price // max(1, number)

        if not root:
            return 0, 0

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


    def get_nodes(self, id : str) -> Dict:

        root = self.products.find_one({'id': id}, {'_id': False})
        self.build_node(root)

        return root

    
    def sales(self, date : datetime) -> Dict:
        return {}


    def statistics(self, id : str, date_start : datetime, date_end : datetime) -> Dict:
        return {
            'not_empty': True
        }
