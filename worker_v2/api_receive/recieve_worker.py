"""Worker to process data from front."""

import logging

import pika

from api_recieve.html_render.html_generator import handle_frontend_callback
from api_recieve.settings.config import settings

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)


def rabbit_init() -> pika.adapters.blocking_connection.BlockingChannel:
    """Connect to rabbit and return channel.

    Returns:
        pika.adapters.blocking_connection.BlockingChannel
    """
    url_parameters = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(url_parameters)
    channel = connection.channel()
    channel.queue_declare(settings.rabbitmq_queue)
    channel.queue_declare(settings.rabbitmq_queue_html_to_pdf)
    channel.queue_declare(settings.rabbitmq_queue_send_email)
    logger.debug('Got channel and queue')
    return channel


def main() -> None:
    """Process to get data from frontend."""
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger.debug('Starting collect data from frontend.')
    channel = rabbit_init()
    channel.basic_consume(
        queue=settings.rabbitmq_queue,
        on_message_callback=handle_frontend_callback,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()


if __name__ == '__main__':
    main()
