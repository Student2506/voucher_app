"""Worker to generate html."""

import json
import logging
from distutils.dir_util import copy_tree
from shutil import rmtree
from tempfile import mkdtemp

import pika

from database import database_classes, models
from html_generation import html_generator
from pdf_generation import pdf_generator
from send_to_email import email_communication
from settings.config import settings
from zip_generation import zip_generator

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)


def get_stocks(stock_id: str) -> list[models.TblStock]:
    """Get stocks.

    Args:
        stock_id: str - stock to use

    Returns:
        list[TblStock] - stocks
    """
    mssql_instance = database_classes.MSSQLDB(settings.mssql_url, settings.mssql_password)
    return list(mssql_instance.get_table_stock(stock_id))


def get_templates(template_id: str) -> models.Template | None:
    """Get Template.

    Args:
        template_id: str - id of template

    Returns:
        list[Template] - template list
    """
    postgres_instance = database_classes.PostgresDB(settings.postgres_url, settings.postgres_password)
    return postgres_instance.get_template(template_id)


def html_generation(                        # noqa: WPS213
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
    logger.debug('Invoke callback')
    request = json.loads(body.decode())
    stocks = get_stocks(request.get('order_item'))
    template = get_templates(request.get('template'))
    addresses = request.get('addresses')
    code_type = request.get('codetype', 'barcode')
    html_folder = mkdtemp()
    logger.debug(html_folder)
    copy_tree('templates/static', html_folder)
    if template:
        logger.debug(f'Template is: {template}')
        for stock in stocks:
            html_generator.html_generation(
                template=str(template.template),
                code_to_fill=str(stock.stock_strbarcode),
                folder=html_folder,
                code_type=code_type,
            )
    else:
        logger.error(f'Template: {template}')
        return
    logger.debug('PDF GENERATE')
    pdf_generator.pdf_generation(html_folder)
    logger.debug('ENDPDF')
    if settings.debug:
        return
    logger.debug('ZIP GENERATE')
    file_to_send = zip_generator.generate_zip_file(html_folder)
    logger.debug('SEND EMAIL')
    email_handle = email_communication.EmailWorker()
    email_handle.send_message(addresses, 'Vouchers ordered', file_to_send)
    rmtree(html_folder)


def main() -> None:
    """Process."""
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger.debug('Starting process')
    url_parameters = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(url_parameters)
    channel = connection.channel()
    channel.queue_declare(settings.rabbitmq_queue)
    channel.queue_declare(settings.rabbitmq_queue_html_to_pdf)
    logger.debug('Got channel and queue')
    channel.basic_consume(
        queue=settings.rabbitmq_queue,
        on_message_callback=html_generation,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()


if __name__ == '__main__':
    main()
