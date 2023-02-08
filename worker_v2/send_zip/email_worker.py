"""Main worker to create zip."""
import logging
from functools import partial

import pika
import redis

from queue_handle.receive_email import handle_pdf
from settings.config import settings

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
    channel.queue_declare(settings.rabbitmq_queue_send_email)
    logger.debug('Got channel and queue')
    return channel


def redis_init() -> redis.Redis:            # type: ignore[type-arg]
    """Connect to redis.

    Returns:
        redis.Redis- instance
    """
    return redis.from_url(settings.redis_url)


def main() -> None:
    """Process to get data from frontend."""
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger.debug('Starting collect data from frontend.')
    channel = rabbit_init()
    redis_instance = redis_init()
    handle_pdf_part = partial(handle_pdf, redis=redis_instance)
    channel.basic_consume(
        queue=settings.rabbitmq_queue,
        on_message_callback=handle_pdf_part,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()


if __name__ == '__main__':
    main()
