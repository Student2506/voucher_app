from aiohttp import web

from settings.config import get_logger, settings

logger = get_logger(__name__)


routes = web.RouteTableDef()


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    return web.Response(text='Hello, World')


app = web.Application()
app.add_routes(routes)
web.run_app(app)
print(settings.port_to_listen)
