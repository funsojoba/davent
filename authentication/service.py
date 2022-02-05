from authentication.models import User
from helpers.response import Response


class UserService:
    @classmethod
    def create_user(cls, **kwargs):
        password = kwargs.get("password")
        user = User.objects.create(**kwargs)
        user.set_password(password)
        user.save()

    @classmethod
    def create_admin_user(
        cls,
        first_name,
        last_name,
        email,
        phone_number,
        city,
        state,
        country,
        password,
        **kwargs
    ):
        user = cls.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            city=city,
            state=state,
            country=country,
            user_type="ADMIN",
        )
        cls.set_user_password(user, password)
        return user

    @classmethod
    def create_viewer_user(
        cls,
        first_name,
        last_name,
        email,
        phone_number,
        city,
        state,
        country,
        password,
        **kwargs
    ):
        user = cls.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            city=city,
            state=state,
            country=country,
            user_type="USER",
        )
        cls.set_user_password(user, password)

    @classmethod
    def activate_user(cls, email: str):
        user = User.objects.filter(email=email).first()
        user.is_active = True
        user.save()

    @classmethod
    def set_user_password(cls, user, password):
        user.set_password(password)
        user.save()

    @classmethod
    def update_user(cls, user, **kwargs):
        user = User(**kwargs)
        user.save()
