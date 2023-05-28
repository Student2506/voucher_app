"""Worker to process html to pdf."""

from settings.config import get_logger, settings
from thread_worker.worker import PDFBuilder

logger = get_logger(__name__)


def main() -> None:
    """Process to get data from frontend."""
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
