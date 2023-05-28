"""Main worker to create zip."""

import pika

from settings.config import get_logger, settings
from zip_creation.receive_pdf import handle_pdf

logger = get_logger(__name__)


def rabbit_init() -> pika.adapters.blocking_connection.BlockingChannel:
    """Connect to rabbit and return channel.

    Returns:
        pika.adapters.blocking_connection.BlockingChannel
    """
    url_parameters = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(url_parameters)
    channel = connection.channel()
    channel.queue_declare(settings.rabbitmq_queue_pdf_to_zip)
    logger.debug('Got channel and queue')
    return channel


def main() -> None:
    """Process to get data from frontend."""
    logger.debug('Starting collect data from frontend.')
    channel = rabbit_init()
    channel.basic_consume(
        queue=settings.rabbitmq_queue_pdf_to_zip,
        on_message_callback=handle_pdf,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()


if __name__ == '__main__':
    main()
