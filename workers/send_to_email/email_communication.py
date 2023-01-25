"""Module to use to send email."""
import pathlib
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader, select_autoescape

from settings.config import settings


class EmailWorker:
    """Mail Worker Logic."""

    def __init__(self) -> None:
        """Create instance of MAILWorker."""
        self.server = settings.email_smtp_server
        self.port = settings.email_smtp_port
        self.connection = smtplib.SMTP(self.server, self.port)

    def send_message(
        self,
        recipients: list[str],
        subject: str,
        file_to_attach: str,
        fields: dict[str, str] | None = None,
    ) -> None:
        """Send emails.

        Args:
            recipients: list - List of email reciepents
            subject: str - Subject of email
            file_to_attach: str - Path to zip-archive
            fields: dict - Fields to fill the template
        """
        message = EmailMessage()
        message['From'] = settings.email_user
        message['To'] = ','.join(recipients)
        message['Subject'] = subject

        templates_storage = pathlib.Path() / 'templates'
        env = Environment(
            loader=FileSystemLoader(templates_storage),
            autoescape=select_autoescape(),
        )
        template_rendered = env.get_template('email_template.html').render(
            title=subject,
            # **fields,
        )
        message.add_alternative(template_rendered, subtype='html')
        with open(file_to_attach, 'rb') as fh:
            message.add_attachment(
                fh.read(),
                maintype='application',
                subtype='zip',
                filename=pathlib.Path(file_to_attach).name,
            )
        self.connection.sendmail(settings.email_user, recipients, message.as_string())
        self.connection.close()


if __name__ == '__main__':
    fields = {
        'text': 'Произошло что-то интересное',
        'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png',
    }
    mail_worker = EmailWorker()
    mail_worker.send_message(
        ['Павел Захаров <zpe25@yandex.ru>'],
        'Привет!',
        'mail.html',
        fields,
    )
