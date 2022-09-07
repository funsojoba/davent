from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailManager:
    def __init__(
        self, template, recipients: list = [], subject: str = None, context: dict = {}
    ):
        self.template = template
        self.subject = subject
        self.context = context
        self.recipients = recipients

    def _compose_message(self):
        message = EmailMessage(
            subject=self.subject,
            body=render_to_string(self.template, self.context),
            from_email="support@davent.com",
            to=self.recipients,
        )
        message.content_subtype = "html"
        return message

    def send(self):
        mail = self._compose_message()
        result = mail.send(fail_silently=False)
        return result
