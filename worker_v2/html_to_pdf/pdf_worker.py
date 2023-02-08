"""Worker to process html to pdf."""
import logging

import pika

from html_to_pdf.process_html.tasks import process_html
from html_to_pdf.settings.config import settings

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)


def rabbit_init() -> pika.adapters.blocking_connection.BlockingConnection:
    """Connect to rabbit and return channel.

    Returns:
        pika.adapters.blocking_connection.BlockingConnection
    """
    url_parameters = pika.URLParameters(settings.rabbitmq_url)
    return pika.BlockingConnection(url_parameters)


def main() -> None:
    """Process to get data from frontend."""
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger.debug('Starting collect data from frontend.')
    connection = rabbit_init()
    process_html(connection)


if __name__ == '__main__':
    main()
