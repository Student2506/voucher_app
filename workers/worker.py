"""Worker to generate pdf."""

import json
from tempfile import mkdtemp

import pika

from database.database_classes import MSSQLDB, PostgresDB
from database.models import TblStock, Template
from html_generation import html_generator
from settings.config import settings


def get_stocks(stock_id: str) -> list[TblStock]:
    """Get stocks.

    Args:
        stock_id: str - stock to use

    Returns:
        list[TblStock] - stocks
    """
    mssql_instance = MSSQLDB(settings.mssql_url, settings.mssql_password)
    return list(mssql_instance.get_table_stock(stock_id))


def get_templates(template_id: str) -> Template | None:
    """Get Template.

    Args:
        template_id: str - id of template

    Returns:
        list[Template] - template list
    """
    postgres_instance = PostgresDB(settings.postgres_url, settings.postgres_password)
    return postgres_instance.get_template(template_id)


def pdf_generation(
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
    template = get_templates(request.get('template'))
    html_folder = mkdtemp()
    if template:
        for stock in stocks:
            html_generator.html_generation(
                template=str(template.template),
                code_to_fill=str(stock.stock_strbarcode),
                folder=html_folder,
                code_type='barcode',
            )


def main() -> None:
    """Process."""
    url_parameters = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(url_parameters)
    channel = connection.channel()
    channel.queue_declare(settings.rabbitmq_queue)
    channel.basic_consume(
        queue=settings.rabbitmq_queue,
        on_message_callback=pdf_generation,
        auto_ack=True,
    )
    channel.start_consuming()


if __name__ == '__main__':
    main()
