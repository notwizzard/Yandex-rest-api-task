from aiohttp import web
from components.baseclasses.handler import Handler

def main():
    handler = Handler()
    app = web.Application()
    app.add_routes([web.post('/imports', handler.imports),
                    web.get('/nodes/{id}', handler.nodes),
                    web.get('/sales', handler.sales),
                    web.get('/node/{id}/statistic', handler.statistics),
                    web.delete('/delete/{id}', handler.delete)])
    web.run_app(app, port=80)

if __name__ == '__main__':
    main()