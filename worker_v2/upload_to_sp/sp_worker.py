"""Main worker to create zip."""
from functools import partial

import pika
import redis

from queue_handle.receive_email import collect_email_info
from settings.config import get_logger, settings

logger = get_logger(__name__)


def rabbit_init() -> pika.adapters.blocking_connection.BlockingChannel:
    """Connect to rabbit and return channel.

    Returns:
        pika.adapters.blocking_connection.BlockingChannel
    """
    url_parameters = pika.URLParameters(str(settings.rabbitmq_url))
    connection = pika.BlockingConnection(url_parameters)
    channel = connection.channel()
    channel.queue_declare(settings.rabbitmq_queue_send_sharepoint)
    logger.debug('Got channel and queue')
    return channel


def redis_init() -> redis.Redis:  # type: ignore[type-arg]
    """Connect to redis.

    Returns:
        redis.Redis- instance
    """
    return redis.from_url(str(settings.redis_url), decode_responses=True)


def main() -> None:
    """Process to get data from frontend."""
    logger.debug('Starting collect data from frontend.')
    channel = rabbit_init()
    redis_instance = redis_init()
    collect_email_info_part = partial(collect_email_info, redis=redis_instance)
    channel.basic_consume(
        queue=settings.rabbitmq_queue_send_sharepoint,
        on_message_callback=collect_email_info_part,
        auto_ack=True,
    )
    logger.debug('Into consume')
    channel.start_consuming()


if __name__ == '__main__':
    main()
