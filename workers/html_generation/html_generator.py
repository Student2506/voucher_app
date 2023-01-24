"""Module responible to assembly htmls."""

from pathlib import Path

import qrcode
from barcode import Code128
from barcode.writer import SVGWriter
from jinja2 import Environment, PackageLoader, select_autoescape
from qrcode.image.svg import SvgPathImage


def barcode_generation(folder: str, code_to_fill: str) -> Path:
    """Generate barcode type Code128.

    Args:
        folder: str - folder to keep image
        code_to_fill: str - code to include in image

    Returns:
        Path - filename path to generated image
    """
    filename = Path(folder) / f'{code_to_fill}.svg'
    with open(filename, 'wb') as fh:
        Code128(str(code_to_fill), writer=SVGWriter()).write(fh)
    return filename


def qr_code_generation(folder: str, code_to_fill: str) -> Path:
    """Generate qrcode.

    Args:
        folder: str - folder to keep image
        code_to_fill: str - code to include in image

    Returns:
        Path - filename path to generated image
    """
    filename = Path(folder) / f'{code_to_fill}.svg'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
        image_factory=SvgPathImage,
    )
    qr.add_data(str(code_to_fill))
    qr.make(fit=True)
    img = qr.make_image(fill_color=(224, 0, 63), back_color='white')
    img.save(filename)
    return filename


def html_generation(
    template: str,
    code_to_fill: str,
    folder: str,
    code_type: str,
) -> None:
    """Generate html files to preprocess.

    Args:
        template: str - template part to include in common part
        code_to_fill: str - code to generate voucher upon
        folder: str - folder to keep templates
        code_type: str - type of code generator
    """
    env = Environment(
        loader=PackageLoader('worker'),
        autoescape=select_autoescape(),
    )
    base_template = env.get_template('refactorOrder_template.html')
    barcode_filename: Path
    if code_type == 'barcode':
        barcode_filename = barcode_generation(folder, code_to_fill)
    else:
        barcode_filename = qr_code_generation(folder, code_to_fill)
    base_template.render(
        barcode=barcode_filename,
    )
