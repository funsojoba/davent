from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response
from .serializers import RegisterUserSerializer, UserSerializer

from .service import UserService


class UserViewSet(viewsets.ViewSet):
    @action(methods=["post"], url_path="register/admin", detail=True)
    def create_admin_user(self, request):
        user = request.user
        data = request.data
        serializer = RegisterUserSerializer(data=request.data).data

        serializer.is_valid(raise_exception=True)

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise ValueError("password and confirm password do not match")

        user = UserService.create_admin_user(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            password=data.get("password"),
        )
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)
