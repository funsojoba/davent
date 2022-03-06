from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response

from .service import EventService, EventCategoryService
from . import serializers


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
        return Response(data=dict(event=serializers.GetEventSerializer(service_response, many=True).data))

    @swagger_auto_schema(
        operation_description="Register for Event",
        operation_summary="Register for Event",
        tags=["Event"],
    )
    @action(detail=False, methods=["post"], url_path="register/(?P<pk>[a-z,A-Z,0-9]+)")
    def register_event(self, request, pk):
        service_response = EventService.register_event(request.user, pk)
        return Response(data=dict(event=serializers.GetEventCategorySerializer(service_response).data))


class AdminEventViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        operation_description="Create Event",
        operation_summary="Create Event",
        tags=["Event"],
    )
    def create(self, request):
        serializer = serializers.CreateEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors=serializer.errors)
        
        service_response = EventService.create_event(
            request.user, **serializer.data)
        return Response(data=dict(event=serializers.GetEventCategorySerializer(service_response).data))


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
            request.user, name=serializer.data.get("name"))
        return Response(data=dict(event=serializers.GetEventCategorySerializer(service_response).data))

    @swagger_auto_schema(
        operation_description="List Event Category",
        operation_summary="List Event Category",
        tags=["Event Category"],
    )
    def list(self, request):
        service_response = EventCategoryService.list_event_category(
            request.user)
        serializer = serializers.GetEventCategorySerializer(
            service_response, many=True).data

        return Response(data=dict(event=serializer))
