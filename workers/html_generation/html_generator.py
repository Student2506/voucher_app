"""Module responible to assembly htmls."""

import logging
from io import BytesIO
from pathlib import Path

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from jinja2 import Environment, PackageLoader, select_autoescape
from PIL import Image

from database.models import Template

logger = logging.getLogger(__name__)
ROTATE_DEGRE = -90
NEW_SIZE = 90, 290


def barcode_generation(folder: str, code_to_fill: str) -> Path:
    """Generate barcode type Code128.

    Args:
        folder: str - folder to keep image
        code_to_fill: str - code to include in image

    Returns:
        Path - filename path to generated image
    """
    filename = Path(folder) / f'{code_to_fill}.png'
    rv = BytesIO()
    barcode = Code128(str(code_to_fill), writer=ImageWriter(format='PNG'))
    barcode.write(rv, {'module_height': 8, 'quiet_zone': 3, 'font_size': 7, 'text_distance': 3})
    with Image.open(rv, formats=('PNG',)) as im:
        im = im.rotate(ROTATE_DEGRE, expand=True)
        im = im.resize(NEW_SIZE)
        im.save(filename)
    return filename


def qr_code_generation(folder: str, code_to_fill: str) -> Path:
    """Generate qrcode.

    Args:
        folder: str - folder to keep image
        code_to_fill: str - code to include in image

    Returns:
        Path - filename path to generated image
    """
    back_color = 'white'
    filename = Path(folder) / f'{code_to_fill}.png'
    base_img = Image.new('RGB', NEW_SIZE)
    dimensions = [0, 0, base_img.size[0], base_img.size[1]]
    base_img.paste(back_color, dimensions)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=4,
    )
    qr.add_data(str(code_to_fill))
    qr.make(fit=True)
    img = qr.make_image(fill_color=(224, 0, 63), back_color=back_color)
    img = img.crop((10, 10, 78, 78))
    img = img.rotate(ROTATE_DEGRE)
    size = NEW_SIZE[1]/2 - img.size[1]/2
    base_img.paste(img, (10, round(size)))
    base_img.save(filename)
    return filename


def html_generation(
    template: Template,
    code_to_fill: str,
    folder: str,
    code_type: str,
) -> None:
    """Generate html files to preprocess.

    Args:
        template: Template - template part to include in common part
        code_to_fill: str - code to generate voucher upon
        folder: str - folder to keep templates
        code_type: str - type of code generator
    """
    with open(Path('templates') / 'refactorOrder_template.html', 'w') as user_template:
        template = template.template.replace('<br />', '')
        user_template.writelines(template)
    base_template = Environment(
        loader=PackageLoader('worker_front_to_html'),
        autoescape=select_autoescape(),
    ).get_template('refactorOrder_template.html')
    logger.debug(f'base_template: {base_template}')
    barcode_filename: Path
    if not code_type or code_type == 'barcode':
        barcode_filename = barcode_generation(folder, code_to_fill)
    if code_type == 'qrcode':
        barcode_filename = qr_code_generation(folder, code_to_fill)
    html_content = base_template.render(
        barcode=barcode_filename.name,
    )
    logger.debug(f'html_content {html_content}')
    with open(Path(folder) / f'{code_to_fill}.html', 'w') as fh:
        fh.write(html_content)
    with open(Path('templates') / 'refactorOrder_template.html', 'w'):
        logger.debug('Cleanup file')
