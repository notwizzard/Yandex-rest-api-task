from aiohttp import web
import json
from typing import Dict
import dateutil.parser
from datetime import datetime
from .baseclasses.importRequest import ImportRequest
from .baseclasses.errorList import ErrorList
from .baseclasses.database import Database
from .schemas.ShopUnitImportRequest import SHOP_UNIT_IMPORT_REQUEST 

class Handler:

    def __init__(self) -> None:
        self.database = Database()

    async def imports(self, r):
        request_json : Dict
        try:
            request_json = await r.json()
        except:
            error = ErrorList.validation.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])

        request = ImportRequest(request_json)
        if not request.validate(SHOP_UNIT_IMPORT_REQUEST):
            return web.Response(text=json.dumps(request.error), status=request.error['code'])  

        self.database.import_data(request.data)

        return web.Response(status=200)

    async def delete(self, request):
        id : str
        try:
            id = request.match_info['id']
        except:
            error = ErrorList.validation.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])

        if not self.database.delete_data(id):
            error = ErrorList.existence.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])
        
        return web.Response(status=200)

    async def nodes(self, request):
        id : str
        try:
            id = request.match_info['id']
        except:
            error = ErrorList.validation.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])

        tree = self.database.get_nodes(request.match_info['id'])
        if tree == None:
            error = ErrorList.existence.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])
        
        return web.Response(text=json.dumps(tree, ensure_ascii=False), status=200)

    async def sales(self, request):
        date : datetime
        try:
            date_str = request.rel_url.query['date']
            date = dateutil.parser.isoparse(date_str)
        except:
            error = ErrorList.validation.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])
        
        result = self.database.sales(date)

        return web.Response(text=json.dumps(result, ensure_ascii=False), status=200)

    async def statistics(self, request):
        date_start : datetime
        date_end : datetime
        id : str
        try:
            date_start_str = request.rel_url.query['dateStart']
            date_end_str = request.rel_url.query['dateEnd']
            date_start = dateutil.parser.isoparse(date_start_str)
            date_end = dateutil.parser.isoparse(date_end_str)
            id = request.match_info['id']
        except:
            error = ErrorList.validation.value
            return web.Response(text=json.dumps(error, ensure_ascii=False), status=error['code'])
        
        result = self.database.statistics(id, date_start, date_end)

        return web.Response(text=json.dumps(result, ensure_ascii=False), status=200)
