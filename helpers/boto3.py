import os
import uuid
import boto3
import logging
from django.conf import settings
from botocore.exceptions import ClientError


class AWSFileUploadManger:
    def __init__(self, append_folder=None):
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self.key = settings.AWS_SECRET_ACCESS_KEY
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        self.obj = self.s3.Object(self.bucket, self.key)
        self.folder = f"backend-{settings.ENVIRONMENT}"
        if append_folder:
            self.folder += append_folder

    def build_file_name(self, file_name):
        extension = file_name.split(".")[-1]
        return f"{uuid.uuid4().hex}.{extension}"

    def upload_file_object(self, file_object, file_name):
        key = self.build_file_name(file_name)
        self.s3.Bucket(self.bucket).put_object(
            Key=f"{self.folder}/{key}", Body=file_object, ACL="public-read"
        )
        return f"https://{self.bucket}.s3.amazonaws.com/{self.folder}/{key}"
