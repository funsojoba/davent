from authentication.models import User
from helpers.response import Response
from helpers.generate_otp import get_otp
from helpers.cache_manager import CacheManager
from .serializers import UserSerializer
from notification.service import EmailService


class UserService:
    @classmethod
    def _create_user(cls, user_type, **kwargs):
        otp = get_otp()
        password = kwargs.get("password")

        user = User.objects.create(
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            phone_number=kwargs.get("phone_number"),
            email=kwargs.get("email"),
            avatar=kwargs.get("avatar", ""),
            city=kwargs.get("city"),
            state=kwargs.get("state"),
            country=kwargs.get("country"),
            user_type=user_type,
        )
        user.set_password(password)
        user.save()
        CacheManager.set_key(
            f"user:otp:{otp}",
            {"email": user.email},
            86400,
        )
        EmailService.send_async(
            "complete_signup.html",
            "Verify Account",
            [user.email],
            {"first_name": user.first_name, "otp": otp},
        )
        return UserSerializer(instance=user).data

    @classmethod
    def create_admin_user(cls, **kwargs):
        user = cls._create_user("ADMIN", **kwargs)
        return user

    @classmethod
    def create_viewer_user(cls, **kwargs):
        user = cls._create_user("USER", **kwargs)
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

    @classmethod
    def verify_user(cls, otp, email):
        otp = CacheManager.retrieve_key(f"user:otp:{otp}")
        if otp and otp.get("email") == email:
            CacheManager.delete_key(
                f"user:otp:{otp}"
            )  # TODO: delete key is not working for now
            user = User.objects.filter(email=email).first()
            user.is_active = True
            user.save()
            return True
        return False

    @classmethod
    def get_user(cls, **kwargs):
        return User.objects.filter(**kwargs).first()
