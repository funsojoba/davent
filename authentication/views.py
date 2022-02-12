from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response
from .serializers import RegisterUserSerializer, UserSerializer

from .service import UserService


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method="post",
        # request_body=schema_examples.EMAIL_REGISTRATION_INPUT,
        operation_description="Sign up an admin",
        operation_summary="Sign up an admin",
        tags=["Auth"],
        # responses=schema_examples.EMAIL_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="admin-signup")
    def admin_user_signup(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_response = UserService.create_admin_user(**serializer.data)
        return Response(data={"user": serializer.data}, status=status.HTTP_201_CREATED)
