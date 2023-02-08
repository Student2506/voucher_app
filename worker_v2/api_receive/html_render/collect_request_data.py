"""Function to handle html creation."""
import json
import logging
from distutils.dir_util import copy_tree
from shutil import copy
from tempfile import mkdtemp

import pika

from database import database_classes, models
from html_render.html_generator import html_render
from settings.config import settings

logger = logging.getLogger(__name__)


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
    if template.logo_image:
        copy(
            f'media/{template.logo_image}',
            f'{html_folder}/images/logoVoucher.png',
        )
    if template.voucher_image:
        copy(
            f'media/{template.voucher_image}',
            f'{html_folder}/images/voucher.png',
        )
    logger.debug(f'Template is: {template}')
    for index, stock in enumerate(stocks, 1):
        html_render(
            template=template,
            code_to_fill=str(stock.stock_strbarcode),
            folder=html_folder,
            code_type=code_type,
        )
        message = {
            'index': index,
            'file_path': f'{html_folder}/{stock.stock_strbarcode}.html',
            'pdf_path': f'{html_folder}/pdf/{stock.stock_strbarcode}.pdf',
            'total': len(stocks),
        }
        channel.basic_publish(
            exchange='',
            routing_key=settings.rabbitmq_queue_html_to_pdf,
            body=json.dumps(message),
        )


def prepare_send_email(
    addresses: list[str],
    html_folder: str,
    channel: pika.channel.Channel,
) -> None:
    """Collect data for email.

    Args:
        addresses: list[str] - addresses to use for email
        html_folder: str - folder to collect
        channel: pika.channel.Channel - channel to pass data on
    """
    message = {
        'folder': html_folder,
        'addresses': addresses,
    }
    channel.basic_publish(
        exchange='',
        routing_key=settings.rabbitmq_queue_send_email,
        body=json.dumps(message),
    )


def handle_frontend_callback(
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
    stocks = get_stocks(request.get('order_item'))
    template = get_template(request.get('template'))
    addresses = request.get('addresses')
    html_folder = mkdtemp()
    logger.debug(html_folder)
    copy_tree('templates/static', html_folder)
    if template:
        make_html_templates(
            template=template,
            html_folder=html_folder,
            stocks=stocks,
            code_type=request.get('codetype', 'barcode'),
            channel=channel,
        )
        prepare_send_email(
            addresses=addresses, html_folder=html_folder, channel=channel,
        )
    else:
        logger.error(f'Template: {template}')
