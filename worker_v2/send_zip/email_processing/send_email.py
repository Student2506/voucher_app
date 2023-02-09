"""Module to use to send email."""
import logging
import pathlib
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, PackageLoader, select_autoescape

from settings.config import settings

logger = logging.getLogger(__name__)


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
        file_to_attach: str,
    ) -> None:
        """Send emails.

        Args:
            recipients: list - List of email reciepents
            file_to_attach: str - Path to zip-archive
        """
        message = EmailMessage()
        message['From'] = settings.email_user
        message['To'] = recipients
        message['Subject'] = settings.subject_for_email

        env = Environment(
            loader=PackageLoader('email_processing'),
            autoescape=select_autoescape(),
        )
        template_rendered = env.get_template('email_template.html').render(
            title=settings.subject_for_email,
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
        self.connection.sendmail(
            settings.email_user, recipients, message.as_string(),
        )
        self.connection.close()