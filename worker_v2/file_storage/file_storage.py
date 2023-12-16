from aiohttp import web

from settings.config import get_logger, settings

routes = web.RouteTableDef()
logger = get_logger(__name__)


@routes.get('/files/{file_hash}/{file_name}')
async def get_file(request: web.Request) -> web.Response:
    file_hash = request.match_info.get('file_hash')
    file_name = request.match_info.get('file_name')
    logger.debug(f'Getting file: {file_hash}\n{file_name}')
    return web.Response(text='Hi Anya!', content_type='text/html')


def main() -> None:
    app = web.Application()
    web.run_app(app, port=settings.port_to_listen)


if __name__ == '__main__':
    main()
