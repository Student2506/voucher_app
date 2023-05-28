"""Get pdfs and create zip."""
import glob
import json
import os
import subprocess  # noqa: S404
import zipfile
from pathlib import Path

import pika

from log_filters import filters
from settings.config import get_logger, settings

logger = get_logger(__name__)


def split_zip_file(
    zip_folder: Path,
    zip_path: str,
) -> None:
    """Split zip-file in chunks.

    Args:
        zip_folder: Path - Path to keep chunks
        zip_path: str - file to split
    """
    os.mkdir(zip_folder)
    logger.info(zip_folder)
    subprocess.run(             # noqa: S607, S603
        [
            'zipsplit',
            '-n',
            str(settings.volume_size),
            '-b',
            str(zip_folder),
            zip_path,
        ],
    )
    for idx, zip_file in enumerate(glob.glob(f'{zip_folder}/*.zip'), 1):
        name_for_zip = Path(zip_path).stem
        new_name = f'{zip_folder}/{name_for_zip}_{idx:02d}.zip'
        os.rename(zip_file, new_name)
        logger.info(new_name)


def handle_pdf(
    channel: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
) -> None:
    """Process data from frontend.

    Args:
        channel: pika.channel.Channel
        method: pika.spec.Basic.Deliver
        properties: pika.spec.BasicProperties
        body: bytes
    """
    request = json.loads(body.decode())
    filters.request_id.set(request.get('request_id'))
    filters.username.set(request.get('username'))
    logger.debug(request)
    pdf_folder = request.get('pdf_folder')
    with zipfile.ZipFile(request.get('zip_path'), mode='w') as zf:
        for pdf_file in glob.glob(f'{pdf_folder}/*.pdf'):
            zf.write(pdf_file, Path(pdf_file).name)
    zip_folder = Path(request.get('zip_path')).parent / 'zips'
    split_zip_file(zip_folder, request.get('zip_path'))
    channel.basic_publish(
        exchange='',
        routing_key=settings.rabbitmq_queue_send_email,
        body=json.dumps(
            {
                'zip_files': str(zip_folder),
                'folder': str(Path(pdf_folder).parent),
                'request_id': filters.request_id.get(),
                'username': filters.username.get(),
            },
        ),
    )
