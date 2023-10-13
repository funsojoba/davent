import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_signup(client, user):
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


@pytest.mark.django_db
def test_user_login(client, user):
    url = reverse("auth:login")
    data = {
        "email": user.email,
        "password": "testpassword",
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
