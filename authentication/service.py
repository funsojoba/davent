from authentication.models import User
from helper.response import Response


class UserService:
    @classmethod
    def create_user(cls, **kwargs):
        return User.objects.create(**kwargs)
