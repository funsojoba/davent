import pytest
from authentication.models import User


@pytest.fixture(scope="module")
def user():
    user = User.objects.create(
		first_name="John",
		last_name="Doe",
		email="john@test.com",
        phone_number="00000000000",
        city="Test City",
        state="Test State",
        country="Test Country"
        )
    user.set_password("testpassword")
    return user


@pytest.fixture(scope="module")
def admin_user():
    user = User.objects.create(
		first_name="Admin",
		last_name="User",
		email="admin_user@test.com",
        phone_number="00000000001",
        city="Test City",
        state="Test State",
        country="Test Country",
        user_type="ADMIN"
        )
    user.set_password("testpassword")
    return user