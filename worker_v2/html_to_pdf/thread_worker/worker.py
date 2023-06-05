"""Worker to handle threading."""
from threading import Thread, get_ident

import pika

from pdf_render.receive_html import handle_html_to_pdf
from settings.config import get_logger, settings

logger = get_logger(__name__)


class PDFBuilder(Thread):
    """Class to perform heavylifting of converting."""

    def __init__(self) -> None:
        """Create instance of converter."""
        url_parameters = pika.URLParameters(settings.rabbitmq_url)
        self.connection = pika.BlockingConnection(url_parameters)

        logger.debug(f'Thread {get_ident()} Got channel and queue')
        super().__init__()

    def run(self) -> None:
        """Start consuming."""
        self.channel = self.connection.channel()
        self.channel.queue_declare(settings.rabbitmq_queue_html_to_pdf)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=settings.rabbitmq_queue_html_to_pdf,
            on_message_callback=handle_html_to_pdf,
            auto_ack=True,
        )
        logger.debug(f'Thread {get_ident()} In consume')
        self.channel.start_consuming()
