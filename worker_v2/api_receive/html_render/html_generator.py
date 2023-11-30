"""Module responible to assembly htmls."""

from datetime import datetime as dt
from io import BytesIO
from pathlib import Path

import icu
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from jinja2 import Environment, PackageLoader, select_autoescape
from PIL import Image

from database.models import Template
from settings.config import get_logger, settings

logger = get_logger(__name__)
ROTATE_DEGRE = -90
NEW_SIZE = 90, 290


def barcode_render(barcode_filename: Path, code_to_fill: str) -> None:
    """Generate barcode type Code128.

    Args:
        barcode_filename: Path - file to keep image
        code_to_fill: str - code to include in image
    """
    rv = BytesIO()
    barcode = Code128(str(code_to_fill), writer=ImageWriter(format='PNG'))
    barcode.write(
        rv,
        {
            'module_height': 8,
            'quiet_zone': 3,
            'font_size': 7,
            'text_distance': 3,
        },
    )
    with Image.open(rv, formats=('PNG',)) as im:
        im = im.rotate(ROTATE_DEGRE, expand=True)
        im = im.resize(NEW_SIZE)
        im.save(barcode_filename)


def qr_code_render(barcode_filename: Path, code_to_fill: str) -> None:
    """Generate qrcode.

    Args:
        barcode_filename: Path - file to keep image
        code_to_fill: str - code to include in image
    """
    base_img = Image.new('RGB', NEW_SIZE)
    dimensions = [0, 0, base_img.size[0], base_img.size[1]]
    base_img.paste(settings.background_color, dimensions)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=4,
    )
    qr.add_data(str(code_to_fill))
    qr.make(fit=True)
    img = qr.make_image(
        fill_color=settings.foreground_color,
        back_color=settings.background_color,
    )
    img = img.crop((10, 10, 78, 78))
    img = img.rotate(ROTATE_DEGRE)
    size = NEW_SIZE[1] / 2 - img.size[1] / 2
    base_img.paste(img, (10, round(size)))
    base_img.save(barcode_filename)


def html_render(
    template: Template,
    code_to_fill: str,
    folder: str,
    code_type: str,
    expiry_date: str,
) -> None:
    """Generate html files to preprocess.

    Args:
        template: Template - template part to include in common part
        code_to_fill: str - code to generate voucher upon
        folder: str - folder to keep templates
        code_type: str - type of code generator
        expiry_date: str - string with expiry date
    """
    with open(
        Path('templates') / 'refactorOrder_template.html',
        'w',
    ) as user_template:
        user_template.writelines(template.template.replace('<br />', ''))
    barcode_filename = Path(folder) / 'images/shtrih.png'
    if not code_type or code_type == 'barcode':
        barcode_render(barcode_filename, code_to_fill)
    if code_type == 'qrcode':
        qr_code_render(barcode_filename, code_to_fill)
    html_content = (
        Environment(
            loader=PackageLoader('receive_worker'),
            autoescape=select_autoescape(),
        )
        .get_template(
            'refactorOrder_template.html',
        )
        .render(
            barcode=barcode_filename.name,
            expiry_date=get_specific_date(expiry_date),
        )
    )
    file_path = Path(folder) / f'{code_to_fill}.html'
    logger.debug(file_path)
    with open(file_path, 'wb', buffering=0) as fh:
        fh.write(html_content.encode('utf-8'))
    with open(Path('templates') / 'refactorOrder_template.html', 'w'):
        logger.debug('Cleanup file')


def get_specific_date(expiry_date: str) -> str:
    """Return data in format.

    Args:
        expiry_date: str - date from database

    Returns:
        str - data for application format
    """
    df = icu.SimpleDateFormat('dd MMMM YYYY', icu.Locale('ru'))
    return str(df.format(dt.strptime(expiry_date, '%Y-%m-%d')))
