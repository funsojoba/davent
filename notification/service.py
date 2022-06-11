from typing import List
from .tasks import send_mail_async


class EmailService:
    @classmethod
    def send_async(cls, template, subject, recipients: List[str], context):
        send_mail_async.delay(template, subject, recipients, context)
