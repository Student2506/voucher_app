"""Generate zip."""
import glob
import logging
from pathlib import Path
from zipfile import ZipFile

logger = logging.getLogger(__name__)


def generate_zip_file(path: str) -> str:
    """Generate zip-file.

    Args:
        path: str - Folder to look for pdf

    Returns:
        str - path to new zip-file
    """
    logger.debug('INTO ZIP FILE')
    folder = Path(path)
    with ZipFile(str(folder / 'vouchers.zip'), 'w') as zip_file:
        for pdf_file in glob.glob(f'{path}/pdfs/*.pdf'):
            pdf_file_path = Path(pdf_file)
            zip_file.write(pdf_file_path, Path(pdf_file_path).name)
    return str(folder / 'vouchers.zip')
