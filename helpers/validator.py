from rest_framework import status
from django.utils import dateparse

from helpers.exception import CustomApiException


def is_valid_date_format(date):
    """
    Validate that a date is in the correct format
    """

    if date:
        date_value = dateparse.parse_date(date)
        if not date_value:
            raise CustomApiException(
                detail="Date format is incorrect. Use YYYY-MM-DD",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return True
