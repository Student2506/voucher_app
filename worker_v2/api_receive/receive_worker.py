"""Worker to process data from front."""

from functools import partial

import pika
import redis

from html_render.collect_request_data import handle_frontend_callback
from settings.config import get_logger, settings

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = get_logger(__name__)


def redis_init() -> redis.Redis:
    """Connect to Redis.

    Returns:
        redis.Redis - instance
    """
    return redis.from_url(str(settings.redis_url), decode_responses=True)


def rabbit_init() -> pika.adapters.blocking_connection.BlockingChannel:
    """Connect to rabbit and return channel.

    Returns:
        pika.adapters.blocking_connection.BlockingChannel
    """
    url_parameters = pika.URLParameters(str(settings.rabbitmq_url))
    connection = pika.BlockingConnection(url_parameters)
    channel_incoming = connection.channel()
    channel_incoming.queue_declare(settings.rabbitmq_queue_incoming)
    channel_outcoming = connection.channel()
    channel_outcoming.queue_declare(settings.rabbitmq_queue_html_to_pdf)
    logger.debug('Got channel and queue')
    return channel_incoming


def main() -> None:
    """Process to get data from frontend."""
    logger.debug('Starting collect data from frontend.')
    redis_instance = redis_init()
    handle_frontend_part = partial(
        handle_frontend_callback,
        redis_instance=redis_instance,
    )
    channel = rabbit_init()
    channel.basic_consume(
        queue=settings.rabbitmq_queue_incoming,
        on_message_callback=handle_frontend_part,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()


if __name__ == '__main__':
    main()
