"""Module to recieve html and convert to PDF."""

import json
import logging
import os
from datetime import datetime as dt
from pathlib import Path

import pika
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from settings.config import settings

logger = logging.getLogger(__name__)


def create_pdf_file(html_file: str, pdf_file: str) -> None:
    """Generate file from given html.

    Args:
        html_file: str - html-file to render
        pdf_file: str - pdf-file to create
    """
    font_config = FontConfiguration()
    html_folder = Path(html_file).parent
    logger.debug(f'PDF Creation html_folder: {html_folder}')
    logger.debug(f'PDF Creation html_file: {html_file}')
    logger.debug(f'PDF Creation pdf_file: {pdf_file}')
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
    pdf_folder = Path(request.get('pdf_path')).parent
    os.makedirs(pdf_folder, exist_ok=True)
    create_pdf_file(
        html_file=request.get('file_path'),
        pdf_file=request.get('pdf_path'),
    )
    if request.get('index') == request.get('total'):
        current_time = dt.now().strftime('%d.%m.%Y_%H%M')
        message = {
            'pdf_folder': str(pdf_folder),
            'zip_path': f'{pdf_folder.parent}/vouchers_{current_time}.zip',
        }
        logger.debug(f'Outgoing message: {message}')
        channel.basic_publish(
            exchange='',
            routing_key=settings.rabbitmq_queue_pdf_to_zip,
            body=json.dumps(message),
        )
