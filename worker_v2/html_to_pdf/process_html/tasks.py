"""Module to create task to process."""
import logging

from pika.adapters.blocking_connection import BlockingConnection

from html_to_pdf.receive_html import handle_html_to_pdf
from html_to_pdf.settings.config import settings

logger = logging.getLogger(__name__)


def process_html(connection: BlockingConnection) -> None:
    """Worker to start conversation.

    Args:
        connection: BlockingConnection - connection to use
    """
    channel = connection.channel()
    channel.queue_declare(settings.rabbitmq_queue_html_to_pdf)
    logger.debug('Got channel and queue')
    channel.basic_consume(
        queue=settings.rabbitmq_queue_html_to_pdf,
        on_message_callback=handle_html_to_pdf,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()
