"""Function to handle html creation."""
import json
from pathlib import Path
from shutil import copy, copytree
from tempfile import mkdtemp
from typing import Any

import pika
import redis

from database import database_classes, models
from html_render.html_generator import html_render
from log_filters import filters
from settings.config import get_logger, settings

logger = get_logger(__name__)


def get_stocks(stock_id: str) -> list[models.TblStock]:
    """Get stocks.

    Args:
        stock_id: str - stock to use

    Returns:
        list[TblStock] - stocks
    """
    mssql_instance = database_classes.MSSQLDB(
        settings.mssql_url, settings.mssql_password,
    )
    return list(mssql_instance.get_table_stock(stock_id))


def get_template(template_id: str) -> models.Template | None:
    """Get Template.

    Args:
        template_id: str - id of template

    Returns:
        Template - template object
    """
    postgres_instance = database_classes.PostgresDB(
        settings.postgres_url, settings.postgres_password,
    )
    return postgres_instance.get_template(template_id)


def make_html_templates(
    template: models.Template,
    html_folder: str,
    stocks: models.TblStock,
    code_type: str,
    channel: pika.channel.Channel,
) -> None:
    """Create html files.

    Args:
        template: models.Template - html-template to use
        html_folder: str - folder to keep local html-files
        stocks: models.TblStock - data about barcodes to generate
        code_type: str - code type (barcode or qrcode)
        channel: pika.channel.Channel - channel to pass data on
    """
    (Path(html_folder) / 'images').mkdir(exist_ok=True)

    logger.debug(f'Template is: {template}')
    for stock_to_render in stocks:
        if template.logo_image:
            copy(
                f'media/{template.logo_image}',
                f'{html_folder}/{stock_to_render.stock_strbarcode}/images/logoVoucher.png',
            )
        if template.voucher_image:
            copy(
                f'media/{template.voucher_image}',
                f'{html_folder}/{stock_to_render.stock_strbarcode}/images/voucher.png',
            )
        html_render(
            template=template,
            code_to_fill=str(stock_to_render.stock_strbarcode),
            folder=f'{html_folder}/{stock_to_render.stock_strbarcode}',
            code_type=code_type,
            expiry_date=stock_to_render.expiry_date.strftime('%Y-%m-%d'),
        )

    for index, stock in enumerate(stocks, 1):
        message = {
            'index': index,
            'file_path': f'{html_folder}/{stock.stock_strbarcode}/{stock.stock_strbarcode}.html',
            'pdf_path': f'{html_folder}/pdf/{stock.stock_strbarcode}.pdf',
            'total': len(stocks),
            'request_id': filters.request_id.get(),
            'username': filters.username.get(),
        }
        logger.debug(f'Outgoing message: {message}')
        channel.basic_publish(
            exchange='',
            routing_key=settings.rabbitmq_queue_html_to_pdf,
            body=json.dumps(message),
        )


def prepare_send_email(
    addresses: list[str],
    html_folder: str,
    redis_instance: redis.Redis,
) -> None:
    """Collect data for email.

    Args:
        addresses: list[str] - addresses to use for email
        html_folder: str - folder to collect
        redis_instance: redis.Redis
    """
    redis_instance.hset(html_folder, 'recipients', ','.join(addresses))


def handle_frontend_callback(
    channel: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
    redis_instance: redis.Redis,
) -> None:
    """Process data from frontend.

    Args:
        channel: pika.channel.Channel
        method: pika.spec.Basic.Deliver
        properties: pika.spec.BasicProperties
        body: bytes
        redis_instance: redis.Redis
    """
    request = json.loads(body.decode())
    filters.request_id.set(request.get('request_id'))
    filters.username.set(request.get('username'))
    logger.info(f'Incoming initial request: {request}')
    template = get_template(request.get('template'))
    html_folder = mkdtemp()
    copy_data_to_storage(request, html_folder)
    if template:
        make_html_templates(
            template=template,
            html_folder=html_folder,
            stocks=get_stocks(request.get('order_item')),
            code_type=request.get('codetype', 'barcode'),
            channel=channel,
        )
        prepare_send_email(
            addresses=request.get('addresses'),
            html_folder=html_folder,
            redis_instance=redis_instance,
        )
    else:
        logger.error(f'Template: {template}')


def copy_data_to_storage(request: dict[Any, Any], html_folder: str) -> None:
    """Secondary function to create data storage.

    Args:
        request: dict[Any, Any] - data to process
        html_folder: str - Path to create folders
    """
    (Path(html_folder) / 'pdf').mkdir()
    logger.info(html_folder)
    for stock in get_stocks(request.get('order_item')):
        path = Path(html_folder) / stock.stock_strbarcode
        copytree('templates/static/', path)
