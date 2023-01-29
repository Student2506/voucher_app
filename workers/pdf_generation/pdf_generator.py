"""Convert HTML to PDF."""
import glob
import logging
import os
from pathlib import Path

from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

logger = logging.getLogger(__name__)


def create_pdf_file(html_file: str, pdf_file: str) -> None:
    """Generate file from given html.

    Args:
        html_file: str - html-file to render
        pdf_file: str - pdf-file to create
    """
    font_config = FontConfiguration()
    html_folder = Path(html_file).parent
    logger.debug(f'PDF Creation html_folder: {html_folder}')
    logger.debug(f'PDF Creation html_file: {html_file}')
    logger.debug(f'PDF Creation pdf_file: {pdf_file}')
    HTML(html_file).write_pdf(
        pdf_file,
        font_config=font_config,
    )


def pdf_generation(html_path: str) -> None:
    """Generate pdf from html by provided path.

    Args:
        html_path: str - path to fetch html from
    """
    html_file_names = glob.glob(f'{html_path}/*.html')
    pdf_folder = Path(html_path) / 'pdfs'
    os.makedirs(pdf_folder, exist_ok=True)
    for html_file in html_file_names:
        base_name = Path(html_file).stem
        pdf_file = str(pdf_folder / f'{base_name}.pdf')
        create_pdf_file(html_file=html_file, pdf_file=pdf_file)
