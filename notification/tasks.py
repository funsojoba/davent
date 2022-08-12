import smtplib
from typing import List
from celery import shared_task
from notification.utils import EmailManager


@shared_task(
    bind=True,
    autoretry_for=(smtplib.SMTPException,),
)
def send_mail_async(self, template, recipients: List[str], subject, context):
    mail = EmailManager(
        template=template, 
        recipients=recipients, 
        subject=subject, 
        context=context
    )
    mail.send()
