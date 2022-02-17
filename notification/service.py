from .tasks import send_mail_async


class EmailService:
    def send_async(self, template, recipients, subject, context):
        send_mail_async.delay(template, recipients, subject, context)
