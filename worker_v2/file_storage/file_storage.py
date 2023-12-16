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
    logger.debug(f'Getting file: {file_hash}\n{file_name}')
    result = await request.app['redis'].exists(file_hash)
    if result != 1:
        raise web.HTTPNotFound()

    filename = await request.app['redis'].get(file_hash)
    logger.debug(filename)
    filename = Path('storage') / filename
    file_size = filename.stat().st_size
    logger.debug(
        f'File {filename} exists: {filename.exists()}\nand has stats {file_size}'
    )
    response = web.StreamResponse()

    response.headers['Content-Disposition'] = 'attachment; filename=bububbu.zip'
    # response.headers[
    # 'Content-Disposition'
    # ] = f'attachment; filename=\"{quote_plus(file_name.encode("utf-8"))}.zip\"'
    response.headers['Content-Length'] = str(file_size)
    response.headers['Transfer-Encoding'] = 'deflate; chunked'
    response.headers['Connection'] = 'keep-alive'
    logger.debug(response)
    await response.prepare(request)

    async with aiofiles.open(filename) as fh:
        while True:
            next_piece = await fh.read(size=settings.chunk_size)
            if not next_piece:
                break
            await response.write(next_piece)
    await response.write_eof()

    logger.debug(result)
    # return web.Response(text='Hi Anya!')


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
