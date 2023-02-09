"""Module to process messages to send."""
import glob
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
    message = redis.hgetall(request.get('folder'))
    redis.hdel(request.get('folder'), 'recipients')
    logger.debug(message)
    zip_folder = request.get('zip_files')
    for file_name in glob.glob(f'{zip_folder}/*.zip'):
        message['file_to_attach'] = file_name
        logger.debug(message)
        message_formated = CompleteMessage.parse_obj(message)
        EmailWorker().send_message(**message_formated.dict())
