"""Module to recieve html and convert to PDF."""

import json
from datetime import datetime as dt
from pathlib import Path

import pika
import redis
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from log_filters import filters
from settings.config import get_logger, settings

logger = get_logger(__name__)


def create_pdf_file(html_file: str, pdf_file: str) -> None:
    """Generate file from given html.

    Args:
        html_file: str - html-file to render
        pdf_file: str - pdf-file to create
    """
    font_config = FontConfiguration()

    HTML(html_file).write_pdf(
        pdf_file,
        font_config=font_config,
    )


def handle_html_to_pdf(
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
    pdf_folder = Path(request.get('pdf_path')).parent
    logger.debug(request)
    create_pdf_file(
        html_file=request.get('file_path'),
        pdf_file=request.get('pdf_path'),
    )
    redis_instance = redis.from_url(settings.redis_url, decode_responses=True)
    redis_instance.hincrby(str(pdf_folder.parent), 'count')
    if (                                                        # noqa: WPS337
        str(redis_instance.hget(str(pdf_folder.parent), 'count')) ==
        str(request.get('total'))
    ):
        current_time = dt.now().strftime('%d.%m.%Y_%H%M')
        message = {
            'pdf_folder': str(pdf_folder),
            'zip_path': f'{pdf_folder.parent}/vouchers_{current_time}.zip',
            'request_id': filters.request_id.get(),
            'username': filters.username.get(),
        }
        logger.debug(f'Outgoing message: {message}')
        channel.basic_publish(
            exchange='',
            routing_key=settings.rabbitmq_queue_pdf_to_zip,
            body=json.dumps(message),
        )
