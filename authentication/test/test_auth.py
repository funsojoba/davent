import pytest
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from authentication.models import User

from rest_framework.test import APIClient


#import unittest
client = APIClient()


class TestAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone_number="00000000000",
            city="Test City",
            state="Test State",
            country="Test Country"
            )
        self.user.set_password("testpassword")
        self.user.save()

    def test_user_signup_success(self): 
        url = "/api/v1/auth/signup"
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
        response = client.post(url, data, format='json')
        assert response.data['message'] == "success"
        assert response.data["data"]["email"] == "new_user@example.com"
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_user_signup_failure(self): 
        url = "/api/v1/auth/signup"
        data = {
            "email": "new_user@example.com",
            "password": "testpassword",
            "last_name": "User",
            "phone_number": "1234567890",
            "city": "Test City",
            "state": "Test State",
            "country": "Test Country",
        }
        response = client.post(url, data, format='json')
        assert response.data['first_name'] == ['This field is required.']
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_user_login_success(self): 
        url = "/api/v1/auth/login"
        data = {
            "email": self.user.email,
            "password": "testpassword",
        }
        response = client.post(url, data)
        assert response.data['message'] == 'success'
        assert response.status_code == status.HTTP_200_OK
    
    def test_user_login_failure(self): 
        url = "/api/v1/auth/login"
        data = {
            "email": "random@email.com",
            "password": "testpassword",
        }
        response = client.post(url, data)

        assert response.data['message'] == 'failure'
        assert response.data["errors"] == {'error': 'User does not exist'}
        assert response.status_code == status.HTTP_400_BAD_REQUEST
