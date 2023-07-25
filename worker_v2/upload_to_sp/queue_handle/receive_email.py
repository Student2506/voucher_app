"""Module to process messages to send."""
import glob
import json
import shutil
from datetime import datetime as dt
from pathlib import Path

import pika
from pydantic import BaseModel
from redis import Redis
from sp_processing.send_sharepoint import SharePoint

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
    new_folder = f'vouchers_{dt.now().strftime("%Y.%m.%d_%H.%M.%S")}'
    with open(request.get('zip_file'), 'rb') as fh:
        zip_file = fh.read()
    share = SharePoint()
    share.create_folder(new_folder)
    new_archive = share.upload_file(Path(request.get('zip_file')).name, new_folder, zip_file)
    message['file_to_attach'] = new_archive
    logger.debug(message)
    message_formated = CompleteMessage.parse_obj(message)
    EmailWorker().send_message_with_link(**message_formated.dict())
    shutil.rmtree(request.get('folder'))
    folders = glob.glob('/tmp/weasyprint-*')
    for folder in folders:
        shutil.rmtree(folder)
