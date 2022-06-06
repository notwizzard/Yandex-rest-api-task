from aiohttp import web
from datetime import datetime
import json
from .baseclasses.importRequest import ImportRequest
from .baseclasses.database import Database
from .schemas.ShopUnitImportRequest import SHOP_UNIT_IMPORT_REQUEST 

class Handler:

    def __init__(self):
        self.database = Database()

    async def imports(self, r):
        request = ImportRequest(await r.json())
        if not request.validate(SHOP_UNIT_IMPORT_REQUEST):
            return web.Response(text=json.dumps(request.error), status=request.error["code"])  
        
        if not self.database.add_data(request.data):
            print(self.database.error)
            return web.Response(status=500)    

        return web.Response(status=200)
        