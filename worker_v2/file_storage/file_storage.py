import asyncio
from datetime import datetime as dt
from pathlib import Path
from urllib.parse import quote_plus

import aiofiles
from aiohttp import streamer, web

from settings.config import get_logger, settings
from utils.redis_handle import redis_context

logger = get_logger(__name__)
routes = web.RouteTableDef()


@streamer
async def file_sender(writer, file_path):
    with open(file_path, 'rb') as f:
        chunk = f.read(2**16)
        while chunk:
            await writer.write(chunk)
            chunk = f.read(2**16)


@routes.get('/files/v2/{file_hash}/{file_name}')
async def download_file(request: web.Request) -> web.Response:
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
    filename_encoded = quote_plus(file_name.encode("utf-8"))
    headers = dict()
    headers['Content-Disposition'] = f'attachment; filename={filename_encoded}'
    return web.Response(body=file_sender(file_path=file_path), headers=headers)


@routes.get('/files/{file_hash}/{file_name}')
async def get_file(request: web.Request) -> web.StreamResponse():
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
    response = web.StreamResponse()
    filename_encoded = quote_plus(file_name.encode("utf-8"))
    response.headers['Content-Disposition'] = f'attachment; filename={filename_encoded}'
    response.headers['Transfer-Encoding'] = 'chunked'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Content-Type'] = 'zipFile'
    await response.prepare(request)
    try:
        async with aiofiles.open(filename, 'rb') as fh:
            next_piece = await fh.read()
            await asyncio.sleep(1)
            await response.write(next_piece)
    except Exception as e:
        logger.error(str(e))
    finally:
        logger.debug('Done transfer')
        await response.write_eof()

    return response


@routes.get('/')
async def hello(request: web.Request) -> web.Response:
    return web.Response(text='Hello, Aiohttp!')


async def webapp() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    app.cleanup_ctx.append(redis_context)

    return app


if __name__ == '__main__':
    web.run_app(webapp(), port=settings.port_to_listen)
