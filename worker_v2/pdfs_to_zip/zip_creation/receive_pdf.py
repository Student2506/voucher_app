"""Get pdfs and create zip."""
import glob
import json
import logging
import zipfile
from pathlib import Path

import pika

from pdfs_to_zip.settings.config import settings

logger = logging.getLogger(__name__)


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
    pdf_folder = request.get('pdf_folder')
    with zipfile.ZipFile(request.get('zip_path'), mode='w') as zf:
        for pdf_file in glob.glob(f'{pdf_folder}/*.pdf'):
            zf.write(pdf_file)
    message = {
        'zip_files': request.get('zip_path'),
        'folder': str(Path(pdf_folder).parent),
    }
    channel.basic_publish(
        exchange='',
        routing_key=settings.rabbitmq_queue_send_email,
        body=json.dumps(message),
    )
