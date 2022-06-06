from aiohttp import web
from components.handler import Handler

def main():
    handler = Handler()
    app = web.Application()
    app.add_routes([web.post('/imports', handler.imports),
                    web.delete('/delete/{id}', handler.delete),
                    web.get('/nodes/{id}', handler.nodes)])
    web.run_app(app)

if __name__ == '__main__':
    main()