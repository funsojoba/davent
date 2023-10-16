import pytest
from django.urls import reverse
from rest_framework import status

#import unittest



pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestAuthentication:
    pytestmark = pytest.mark.django_db
    def test_user_signup(self, client, user): 
        url = reverse("auth:signup")
        data = {
            "email": "new_user@example.com",
            "password": "testpassword",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "1234567890",
            "city": "Test City",
            "state": "Test State",
            "country": "Test Country",
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_login(self, db, client, user): 
        url = reverse("auth:login")
        data = {
            "email": user.email,
            "password": "testpassword",
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
