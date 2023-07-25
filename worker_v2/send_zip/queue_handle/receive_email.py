"""Module to process messages to send."""
import glob
import json
import shutil

import pika
from pydantic import BaseModel
from redis import Redis

from email_processing.send_email import EmailWorker
from log_filters import filters
from settings.config import get_logger

logger = get_logger(__name__)


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
    filters.request_id.set(request.get('request_id'))
    filters.username.set(request.get('username'))
    logger.debug(request)
    message = redis.hgetall(request.get('folder'))
    redis.hdel(request.get('folder'), 'recipients')
    logger.info(message)
    zip_folder = request.get('zip_files')
    for file_name in glob.glob(f'{zip_folder}/*.zip'):
        message['file_to_attach'] = file_name
        logger.debug(message)
        message_formated = CompleteMessage.parse_obj(message)
        EmailWorker().send_message(**message_formated.dict())
    shutil.rmtree(request.get('folder'))
    folders = glob.glob('/tmp/weasyprint-*')
    for folder in folders:
        shutil.rmtree(folder)
