from aiohttp import web
from datetime import date
import json
from .baseclasses.errorList import ErrorList
from .baseclasses.importRequest import ImportRequest
from .schemas.ShopUnitImportRequest import SHOP_UNIT_IMPORT_REQUEST 

class Handler:

    def __init__(self):
        pass

    async def imports(self, r):
        request = ImportRequest(await r.json())
        if not request.validate(SHOP_UNIT_IMPORT_REQUEST):
            return web.Response(text=json.dumps(request.error), status=request.error['code'])  
        
        return web.Response(status=200)
        