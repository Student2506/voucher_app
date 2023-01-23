"""Worker to generate pdf."""

import json
import os

import pika
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.models import TblStock

RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', None)
MSSQL_URL_PART = os.getenv('MSSQL_URL')
VISTA_URL = f'mssql+pyodbc://{MSSQL_URL_PART}'
VISTA_ENGINE = create_engine(VISTA_URL)


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
    session = Session(VISTA_ENGINE)
    stmt = select(TblStock).where(TblStock.lclientorderitemid == request.get('order_item'))
    for stock in session.scalars(stmt):
        stock.stock_strbarcode   # noqa: WPS428


def main() -> None:
    """Process."""
    connection = pika.BlockingConnection(
        pika.URLParameters(os.getenv('RABBITMQ_URL', None)),
    )
    channel = connection.channel()
    channel.queue_declare(RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=pdf_generation, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
