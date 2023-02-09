"""Module to process messages to send."""
import json
import logging

import pika
from pydantic import BaseModel
from redis import Redis

from email_processing.send_email import EmailWorker

logger = logging.getLogger(__name__)


class CompleteMessage(BaseModel):
    """Class to check that all fields arrived."""

    file_to_attach: str
    recipients: str


def collect_email_info(
    channel: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
    redis: Redis,           # type: ignore[type-arg]
) -> None:
    """Process data from frontend.

    Args:
        channel: pika.channel.Channel
        method: pika.spec.Basic.Deliver
        properties: pika.spec.BasicProperties
        body: bytes
        redis: Redis - to keep data
    """
    request = json.loads(body.decode())
    logger.debug(request)
    folder = request.get('folder')
    message = redis.hgetall(folder)
    redis.hdel(folder)
    logger.debug(message)
    message['file_to_attach'] = request.get('zip_files')
    logger.debug(message)
    message_formated = CompleteMessage.parse_obj(message)
    new_worker = EmailWorker()
    new_worker.send_message(**message_formated.dict())
