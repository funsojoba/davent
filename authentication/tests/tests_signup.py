from django.test import TestCase
from authentication.models import User


class AuthTestCase(TestCase):
    def setUp(self):
            User.objects.create(
                first_name="John",
                last_name="Doe",
                email="john@test.com",
                phone_number="00000000",
                city="New York",
                state="NY",
                country="United States",
            )

    def test_get_user_display_name_success(self):
        """Animals that can speak are correctly identified"""
        john = User.objects.get(email="john@test.com")
        self.assertEqual(john.display_name, 'John Doe')