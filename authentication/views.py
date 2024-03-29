from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser, IsSuperAdmin
from helpers.response import Response
from .serializers import (
    RegisterUserSerializer,
    UserSerializer,
    VerifyAccountSerializer,
    ForgotPasswordSerializer,
    VerifyResetPassword,
    UserSerializer,
    ResetPasswordSerializer,
    LoginUserSerializer,
    UpdateUserSerializer,
    UserAvatarSerializer,
    ActivateUserSerializer,
)

from .service import UserService
from .docs import schema_example

from django.shortcuts import render


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Sign up an admin",
        operation_summary="Sign up an admin",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request_body=RegisterUserSerializer,
    )
    @action(detail=False, methods=["post"], url_path="admin/signup")
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
    @action(detail=False, methods=["post"], url_path="signup", url_name="user-signup")
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
    @action(detail=False, methods=["post"], url_path="verify-otp")
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
        request_body=ForgotPasswordSerializer,
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
        operation_description="Forgot Password",
        operation_summary="Forgot Password",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request_body=ForgotPasswordSerializer,
    )
    @action(detail=False, methods=["post"], url_path="verify-forgot-password")
    def verify_forgot_password_view(self, request):
        serializer = VerifyResetPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.verify_reset_password(
            serializer.data.get("code"), serializer.data.get("email")
        )
        if service_response:
            return Response(data={"VERIFIED": True, "email": serializer.data["email"]})
        return Response(errors={"VERIFIED": False})

    @swagger_auto_schema(
        operation_description="Reset Password",
        operation_summary="Reset Password",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request=ForgotPasswordSerializer,
    )
    @action(detail=False, methods=["post"], url_path="reset-password")
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.reset_password(
            serializer.data.get("password"),
            serializer.data.get("email"),
            serializer.data.get("code"),
        )
        if service_response:
            return Response(data={"PASSWORD_RESET": True})
        return Response(errors={"PASSWORD_RESET": False})

    @swagger_auto_schema(
        operation_description="Login User",
        operation_summary="Login User",
        tags=["Auth"],
        responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
        request_body=LoginUserSerializer,
    )
    @action(detail=False, methods=["post"], url_path="login")
    def login_user(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = UserService.login_user(
            serializer.data.get("email"), serializer.data.get("password")
        )
        return service_response

    @swagger_auto_schema(
        operation_description="Activate User",
        operation_summary="Activate User",
        tags=["Auth"],
        request_body=ActivateUserSerializer,
    )
    @action(detail=False, methods=["post"], url_path="verify-user")
    def activate_user_view(self, request):
        serializer = ActivateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_response = UserService.verify_signed_up_user(
            serializer.data.get("email"), serializer.data.get("otp")
        )
        if service_response:
            return Response(data={"verified": True})
        return Response(data={"verified": False})


class UserViewset(viewsets.ViewSet):
    permission_classes = [IsAdminUser | IsUser]

    @swagger_auto_schema(
        operation_description="User detail",
        operation_summary="User detail",
        tags=["User"],
        responses=schema_example.GET_USER_DATA,
    )
    @action(detail=False, methods=["get"], url_path="me")
    def get_user_profile(self, request):
        user = request.user
        service_response = UserService.get_user(email=user.email)
        serializer = UserSerializer(service_response)
        return Response(data=serializer.data)

    @swagger_auto_schema(
        operation_description="Update user detail",
        operation_summary="Update user detail",
        tags=["User"],
        responses=schema_example.GET_USER_DATA,
    )
    @action(detail=False, methods=["patch"], url_path="me/update")
    def patch(self, request):
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid()
        service_response = UserService.update_user(request.user, **serializer.data)
        return Response(data=UserSerializer(service_response).data)

    @swagger_auto_schema(
        operation_description="Update user Avatar",
        operation_summary="Update user Avatar",
        tags=["User"],
        request_body=UserAvatarSerializer
        # responses=schema_example.GET_USER_DATA,
    )
    @action(detail=False, methods=["post"], url_path="me/avatar")
    def upload_avatar(self, request):
        serializer_ = UserAvatarSerializer(data=request.data)
        serializer_.is_valid(raise_exception=True)
        print(request.data.get("avatar").file, request.data.get("avatar")._name)
        # service_response = UserService.set_user_avatar(
        #     user=request.user, avatar=request.data.get("avatar")
        # )
        service_response = UserService.set_user_avatar_cloudinay(
            user=request.user, avatar=request.data.get("avatar")
        )
        return Response(data=UserSerializer(service_response).data)


class UserAdminViewSet(viewsets.ViewSet):
    permissionn_classes = [IsSuperAdmin]

    def list(self, request):
        service_response = UserService.get_all_users()
        serializer = UserSerializer(service_response)
        return Response(data=serializer.data)


def view_template(request):
    return render(request, template_name="forgot_password.html")
