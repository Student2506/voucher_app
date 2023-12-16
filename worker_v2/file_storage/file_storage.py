from aiohttp import web

from settings.config import get_logger, settings

logger = get_logger(__name__)
routes = web.RouteTableDef()


@routes.get('/files/{file_hash}/{file_name}')
async def get_file(request: web.Request) -> web.Response:
    file_hash = request.match_info.get('file_hash')
    file_name = request.match_info.get('file_name')
    logger.debug(f'Getting file: {file_hash}\n{file_name}')
    return web.Response(text='Hi Anya!')


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    return web.Response(text='Hello, Aiohttp!')


def main() -> None:
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=settings.port_to_listen)


if __name__ == '__main__':
    main()
