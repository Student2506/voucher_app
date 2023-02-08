"""Module to process messages to send."""
import json

import pika
from pydantic import BaseModel
from redis import Redis

from send_zip.email_processing.send_email import EmailWorker


class CompleteMessage(BaseModel):
    """Class to check that all fields arrived."""

    file_to_attach: str
    recipients: str


def handle_pdf(
    channel: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
    redis: Redis[bytes],
) -> None:
    """Process data from frontend.

    Args:
        channel: pika.channel.Channel
        method: pika.spec.Basic.Deliver
        properties: pika.spec.BasicProperties
        body: bytes
        redis: Redis[bytes] - to keep data
    """
    request = json.loads(body.decode())
    folder = request.get('folder')
    if request.get('zip_files', None):
        redis.hset(folder, 'file_to_attach', str(request.get('zip_files')))
    if request.get('addresses', None):
        redis.hset(folder, 'recipients', str(request.get('addresses')))
    message = redis.hgetall(folder)
    message_formated = CompleteMessage.parse_obj(message)
    new_worker = EmailWorker()
    new_worker.send_message(**message_formated)
