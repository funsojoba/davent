from authentication.models import User
from helpers.response import Response
from .serializers import UserSerializer


class UserService:
    @classmethod
    def create_user(cls, **kwargs):
        password = kwargs.get("password")
        user_instance = User.objects.filter(email=kwargs.get("email")).first()
        print(user_instance)
        # if user_instance:
        #     return Response(errors={"email":"user with this email already exist"})
        user = User.objects.create(**kwargs)
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def create_admin_user(cls, **kwargs):
        user = cls.create_user(
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            email=kwargs.get("email"),
            phone_number=kwargs.get("phone_number"),
            city=kwargs.get("city"),
            state=kwargs.get("state"),
            country=kwargs.get("country"),
            password=kwargs.get("password"),
            user_type="ADMIN",
        )
        return user

    @classmethod
    def create_viewer_user(cls, **kwargs):
        user = cls.create_user(
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            email=kwargs.get("email"),
            phone_number=kwargs.get("phone_number"),
            city=kwargs.get("city"),
            state=kwargs.get("state"),
            country=kwargs.get("country"),
            password=kwargs.get("password"),
            user_type="USER",
        )
        return user

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
