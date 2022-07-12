import barcode
import qrcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML, CSS


def generate_pdf(barcode_text, qr_code=False):
    with open('templates/images/barcode.png', 'wb') as f:
        barcode.Code128(
            barcode_text, writer=ImageWriter()
        ).write(f, {'module_height': 10, 'quiet_zone': 5})

    background = Image.new('RGBA', (300, 300), (255, 255, 255, 255))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("arial.ttf", 28)
    if qr_code:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(barcode_text)
        qr.make()
        img_qr = qr.make_image()
        width, height = img_qr.size
        text_width, text_height = draw.textsize(barcode_text, font=font)
        background.paste(img_qr, (0, 5))
        start = (width - text_width)/2
        draw.text(
            (start, 270),
            barcode_text,
            font=font,
            fill=(0, 0, 0)
        )
        background.save('templates/images/qrcode.png')
        html = HTML('templates/default-qr.html')
        css = CSS('templates/default.css')
        html.write_pdf(
            f'pdfs/{barcode_text}.pdf',
            stylesheets=[css]
        )
    else:
        html = HTML('templates/default.html')
        html.write_pdf(
            f'pdfs/{barcode_text}.pdf',
        )


if __name__ == '__main__':
    generate_pdf('000000000000')
