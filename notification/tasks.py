import smtplib
from celery import shared_task
from notification.utils import EmailMessage


@shared_task(
    bind=True,
    autoretry_for=(smtplib.SMTPException,),
)
def send_mail_async(self, template, subject, recipients, context):
    mail = EmailMessage(
        subject=subject, template=template, recipients=recipients, context=context
    )
    mail.send()
