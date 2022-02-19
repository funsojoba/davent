from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response
from .serializers import (
    RegisterUserSerializer,
    UserSerializer,
    VerifyAccountSerializer,
    ForgotPasswordSerializer,
    VerifyResetPassword,
    UserSerializer,
    ResetPasswordSerializer,
)

from .service import UserService
from .docs import schema_example


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Sign up an admin",
        operation_summary="Sign up an admin",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="admin-signup")
    def admin_user_signup(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_response = UserService.create_admin_user(**serializer.data)
        return Response(data=service_response, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Sign up a user",
        operation_summary="Sign up a user",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="signup")
    def user_signup(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.create_viewer_user(**serializer.data)

        return Response(data=service_response, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="verify user",
        operation_summary="verify user",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="verify")
    def verify_user_account(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.verify_user(
            serializer.data.get("otp"), serializer.data.get("email")
        )
        if service_response:
            return Response(data={"VERIFIED": True})
        return Response(errors={"VERIFIED": False})

    @swagger_auto_schema(
        operation_description="Forgot Password",
        operation_summary="Forgot Password",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request=ForgotPasswordSerializer,
    )
    @action(detail=False, methods=["post"], url_path="forgot-password")
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.forogt_password(serializer.data.get("email"))
        if service_response:
            return Response(data={"email": "reset password sent to mail"})
        return Response(errors={"error": "User with this email does not exist"})

    @swagger_auto_schema(
        operation_description="Verify Forgot Password",
        operation_summary="Verify Forgot Password",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request=ForgotPasswordSerializer,
    )
    @action(detail=False, methods=["post"], url_path="verify-forgot-password")
    def verify_forgot_password(self, request):
        serializer = VerifyResetPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.verify_reset_pssword(
            serializer.data.get("code"), serializer.data.get("email")
        )
        if service_response:
            return Response(data={"VERIFIED": True})
        return Response(errors={"VERIFIED": False})

    @swagger_auto_schema(
        operation_description="Reset Password",
        operation_summary="Reset Password",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request=ForgotPasswordSerializer,
    )
    @action(detail=False, methods=["post"], url_path="reset-password")
    def verify_forgot_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.reset_password(
            serializer.data.get("password"), serializer.data.get("email")
        )
        if service_response:
            return Response(data={"PASSWORD_RESET": True})
        return Response(errors={"PASSWORD_RESET": False})
