"""Module to process messages to send."""
import glob
import json
import shutil
from datetime import datetime as dt
from hashlib import md5
from pathlib import Path

import pika
from pydantic import BaseModel
from redis import Redis

from email_processing.send_email import EmailWorker
from local_storage.send_to_local import LocalStorage
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
    redis: Redis,  # type: ignore[type-arg]
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
    new_folder = f'vouchers_{int(dt.now().timestamp())}'
    share = LocalStorage()
    full_path_new_folder = share.create_folder(new_folder)

    new_archive_path = share.upload_file(
        Path(request.get('zip_file')), full_path_new_folder
    )
    logger.debug(new_archive_path)
    logger.debug(md5(new_archive_path.encode('utf-8')).hexdigest())

    message['file_to_attach'] = str(
        Path(new_archive_path) / Path(full_path_new_folder).name
    )
    logger.debug(message['file_to_attach'])
    logger.debug(message)
    message_formated = CompleteMessage.parse_obj(message)
    EmailWorker().send_message_with_link(**message_formated.dict())
    shutil.rmtree(request.get('folder'))
    folders = glob.glob('/tmp/weasyprint-*')
    for folder in folders:
        shutil.rmtree(folder)
