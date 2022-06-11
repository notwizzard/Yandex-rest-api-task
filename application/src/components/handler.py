from aiohttp import web
from datetime import datetime
import json
from .baseclasses.importRequest import ImportRequest
from .baseclasses.database import Database
from .schemas.ShopUnitImportRequest import SHOP_UNIT_IMPORT_REQUEST 

class Handler:

    def __init__(self) -> None:
        self.database = Database()

    async def imports(self, r):
        request = ImportRequest(await r.json())
        if not request.validate(SHOP_UNIT_IMPORT_REQUEST):
            return web.Response(text=json.dumps(request.error), status=request.error["code"])  

        if not self.database.import_data(request.data):
            return web.Response(status=500)  

        return web.Response(status=200)

    async def delete(self, request):

        if not self.database.delete_data(request.match_info["id"]):
            return web.Response(status=404)
        
        return web.Response(status=200)

    async def nodes(self, request):
        tree = self.database.get_nodes(request.match_info["id"])
        if tree == None:
            return web.Response(status=404)
        
        return web.Response(text=json.dumps(tree, ensure_ascii=False), status=200)