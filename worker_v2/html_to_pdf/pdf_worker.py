"""Worker to process html to pdf."""
import logging

from settings.config import settings
from thread_worker.worker import PDFBuilder

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)


def main() -> None:
    """Process to get data from frontend."""
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger.debug('Starting collect data from frontend.')

    threads = []
    for _ in range(settings.threads):
        thread_builder = PDFBuilder()
        thread_builder.start()
        threads.append(thread_builder)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
