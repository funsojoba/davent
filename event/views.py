from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response

from .service import EventService, EventCategoryService
from . import serializers
from authentication.serializers import UserSerializer


class UserEventViewSet(viewsets.ViewSet):
    permission_classes = [IsUser | IsAdminUser]

    @swagger_auto_schema(
        operation_description="List Events",
        operation_summary="List Events",
        tags=["Event"],
    )
    @action(detail=False, methods=["get"], url_path="list")
    def list_events(self, request):
        service_response = EventService.get_events()
        # TODO: filter by location
        return Response(
            data=dict(
                event=serializers.GetEventSerializer(service_response, many=True).data
            )
        )

    @swagger_auto_schema(
        operation_description="Register for Event",
        operation_summary="Register for Event",
        tags=["Event"],
    )
    @action(detail=False, methods=["post"], url_path="register/(?P<pk>[a-z,A-Z,0-9]+)")
    def register_event(self, request, pk):
        service_response = EventService.register_event(request.user, pk)
        return Response(
            data=dict(event=serializers.GetEventSerializer(service_response).data)
        )


class AdminEventViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        operation_description="Create Event",
        operation_summary="Create Event",
        tags=["Event-Admin"],
    )
    def create(self, request):
        serializer = serializers.CreateEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)

        service_response = EventService.create_event(request.user, **serializer.data)
        return Response(
            data=dict(
                event=serializers.GetEventCategorySerializer(service_response).data
            )
        )

    @swagger_auto_schema(
        operation_description="List events",
        operation_summary="List events",
        tags=["Event-Admin"],
    )
    def list(self, request):
        service_response = EventService.get_events(owner=request.user)
        return Response(
            data=dict(
                event=serializers.GetEventSerializer(service_response, many=True).data
            )
        )

    @swagger_auto_schema(
        operation_description="Get all event participants",
        operation_summary="Get all event participants",
        tags=["Event-Admin"],
    )
    @action(
        detail=False, methods=["get"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/participants"
    )
    def get_all_event_participants(self, request, pk=None):
        # TODO: paginate this and also return count
        participants = EventService.get_event_participants(
            user=request.user, event_id=pk
        )
        return Response(
            data=dict(participants=UserSerializer(participants, many=True).data)
        )

    @swagger_auto_schema(
        operation_description="Admin registers users for an event",
        operation_summary="Admin registers users for an event",
        tags=["Event-Admin"],
    )
    @action(
        detail=False, methods=["post"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/register-users"
    )
    def register_users(self, request, pk=None):
        serializer = serializers.AdminRegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        participants = EventService.admin_register_user(
            user_ids=serializer.data.get("user_ids"), event_id=pk
        )
        return Response(
            data=dict(participants=serializers.GetEventSerializer(participants).data)
        )

    @swagger_auto_schema(
        operation_description="Set event status",
        operation_summary="Set event status",
        tags=["Event-Admin"],
    )
    @action(detail=False, methods=["post"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/status")
    def register_event(self, request, pk):

        serializer = serializers.AdminSetEventStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        service_response = EventService.admin_set_event_status(
            pk, serializer.data.get("status")
        )
        return Response(
            data=dict(event=serializers.GetEventSerializer(service_response).data)
        )

    @swagger_auto_schema(
        operation_description="Update event",
        operation_summary="Update event",
        tags=["Event-Admin"],
    )
    def partial_update(self, request, pk=None):
        serializer = serializers.UodateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_response = EventService.update_event(
            event_id=pk, owner=request.user, **serializer.data
        )
        return Response(
            data=dict(event=serializers.GetEventSerializer(service_response).data)
        )


class EventCategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        operation_description="Create Event Category",
        operation_summary="Create Event Category",
        tags=["Event Category"],
    )
    def create(self, request):
        serializer = serializers.EventCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)

        service_response = EventCategoryService.create_event_category(
            request.user, name=serializer.data.get("name")
        )
        return Response(
            data=dict(
                event=serializers.GetEventCategorySerializer(service_response).data
            )
        )

    @swagger_auto_schema(
        operation_description="List Event Category",
        operation_summary="List Event Category",
        tags=["Event Category"],
    )
    def list(self, request):
        service_response = EventCategoryService.list_event_category(request.user)
        serializer = serializers.EventCategorySerializer(
            service_response, many=True
        ).data

        return Response(data=dict(event=serializer))
