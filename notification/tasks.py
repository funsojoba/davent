import smtplib
from celery import shared_task
from notification.utils import EmailManager


@shared_task(
    bind=True,
    autoretry_for=(smtplib.SMTPException,),
)
def send_mail_async(self, template, subject, recipients, context):
    mail = EmailManager(
        template=template, subject=subject, recipients=recipients, context=context
    )
    mail.send()
