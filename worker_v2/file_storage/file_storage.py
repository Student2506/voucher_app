import asyncio
from datetime import datetime as dt
from pathlib import Path
from urllib.parse import quote_plus

import aiofiles
from aiohttp import web

from settings.config import get_logger, settings
from utils.redis_handle import redis_context

logger = get_logger(__name__)
routes = web.RouteTableDef()


@routes.get('/files/{file_hash}/{file_name}')
async def get_file(request: web.Request) -> web.Response:
    file_hash = request.match_info.get('file_hash')
    file_name = request.match_info.get('file_name')
    is_file_exists = await request.app['redis'].exists(file_hash)
    if is_file_exists != 1:
        raise web.HTTPNotFound()
    filename = await request.app['redis'].get(file_hash)
    filename = Path('storage') / filename
    file_size = filename.stat().st_size
    logger.debug(
        f'File {filename} exists: {filename.exists()}\nand has stats {file_size}'
    )
    INTERVAL_SECS = 1
    response = web.StreamResponse()
    response.headers['Content-Type'] = 'text/html'
    await response.prepare(request)
    while True:
        formatted_date = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f'{formatted_date}<br>'
        await response.write(message.encode('utf-8'))
        await asyncio.sleep(INTERVAL_SECS)


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    return web.Response(text='Hello, Aiohttp!')


def main() -> None:
    app = web.Application()
    app.add_routes(routes)
    app.cleanup_ctx.append(redis_context)
    web.run_app(app, port=settings.port_to_listen)


if __name__ == '__main__':
    main()
