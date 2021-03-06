import uuid
from django.conf import settings
from django.contrib.auth.hashers import check_password

from .models import User

from helpers.response import Response
from helpers.generate_otp import get_otp
from helpers.cache_manager import CacheManager
from rest_framework_simplejwt.tokens import RefreshToken

from notification.service import EmailService

from .serializers import UserSerializer


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
            template="complete_signup.html",
            subject="Verify Account",
            recipients=[user.email],
            context={"first_name": user.first_name, "otp": otp},
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
    def get_user(cls, **kwargs):
        return User.objects.filter(**kwargs).first()

    @classmethod
    def verify_user(cls, otp, email):
        otp = CacheManager.retrieve_key(f"user:otp:{otp}")
        if otp and otp.get("email") == email:
            CacheManager.delete_key(
                f"user:otp:{otp}"
            )  # TODO: delete key is not working for now
            user = cls.get_user(email=email).first()
            user.is_active = True
            user.save()
            return True
        return False

    @classmethod
    def forogt_password(cls, email):
        user = cls.get_user(email=email)

        if user:
            code = uuid.uuid4().hex
            verification_link = (
                f"{settings.BASE_URL}/verify-user?code={code}&email={email}"
            )
            CacheManager.set_key(
                f"user:reset_password:{code}",
                {"email": user.email},
                86400,
            )
            EmailService.send_async(
                "forgot_password.html",
                "Forgot Password",
                [email],
                {
                    "first_name": user.first_name.capitalize(),
                    "verification_link": verification_link,
                },
            )
            return True
        return False

    @classmethod
    def verify_reset_pssword(cls, code, email):
        code = CacheManager.retrieve_key(f"user:reset_password:{code}")
        if code and code.get("email") == email:
            CacheManager.delete_key(f"user:reset_password:{code}")
            return True
        return False

    @classmethod
    def reset_password(cls, password, email):
        user = cls.get_user(email=email)
        password = cls.set_user_password(user, password)
        return True

    @classmethod
    def login_user(cls, email, password):
        user = cls.get_user(email=email)

        if user:
            user_password = check_password(password, user.password)

            if not user_password:
                return Response(errors={"error": "incorrect password"})

            token = RefreshToken.for_user(user)
            data = {
                "user": UserSerializer(instance=user).data,
                "token": {"refresh": str(token), "access": str(token.access_token)},
            }
            return Response(data=data)
        return Response(errors={"error": "User does not exist"})

    @classmethod
    def get_all_users(cls):
        return User.objects.all()
