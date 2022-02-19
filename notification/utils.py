from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailManager:
    def __init__(self, template, recipients=[], subject=None, context={}):
        self.template = template
        self.subject = subject
        self.context = context
        self.recipients = recipients

    def _compose_message(self):
        html_content = render_to_string(self.template, self.context)
        text_content = strip_tags(html_content)
        message = EmailMultiAlternatives(
            self.subject,
            text_content,
            settings.EMAIL_FROM,
            self.recipients,
        )
        message.attach_alternative(html_content, "text/html")
        return message

    def send(self):
        mail = self._compose_message()
        result = mail.send(fail_silently=False)
        return result
