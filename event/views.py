from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from django.db.models import Q
from django.utils import timezone


from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response
from helpers.validator import is_valid_date_format

from .service import EventService, EventCategoryService, TicketService
from . import serializers
from authentication.serializers import UserSerializer

from helpers.response import paginate_response


class UserEventViewSet(viewsets.ViewSet):
    permission_classes = [IsUser | IsAdminUser]

    @swagger_auto_schema(
        operation_description="List Events",
        operation_summary="List Events",
        tags=["Event"],
    )
    def list(self, request):
        # Get events around a user that is active and valid date

        today = timezone.now()
        start_date = request.query_params.get("start_date", today)
        event_country = request.query_params.get("event_country", request.user.country)
        event_state = request.query_params.get("event_state", request.user.state)
        event_city = request.query_params.get("event_state", request.user.city)

        if is_valid_date_format(start_date.strftime("%Y-%m-%d")):
            service_response = EventService.get_events().filter(
                # Q(event_state=event_state) |
                # Q(event_country=event_country) |
                Q(event_city=event_city),
                status="ACTIVE",
                start_date__gte=start_date,
            )
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
    @action(
        detail=False, methods=["POST"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/free-register"
    )
    def register_event(self, request, pk):
        service_response = EventService.register_event_free(request.user, pk)
        return Response(
            data=dict(event=serializers.GetEventSerializer(service_response).data)
        )

    @swagger_auto_schema(
        operation_description="Get Event ticket",
        operation_summary="Get Event ticket",
        tags=["Event"],
    )
    @action(detail=False, methods=["GET"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/ticket")
    def event_ticket(self, request, pk):
        service_response = TicketService.get_ticket(user=request.user, event_id=pk)
        return Response(data=serializers.TicketSerializer(service_response).data)

    @swagger_auto_schema(
        operation_description="Get single event detail",
        operation_summary="Get single event detail",
        tags=["Event"],
    )
    def retrieve(self, request, pk):
        service_response = EventService.get_single_event(id=pk)
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
        return Response(data=serializers.GetEventSerializer(service_response).data)

    @swagger_auto_schema(
        operation_description="List events",
        operation_summary="List events",
        tags=["Event-Admin"],
    )
    def list(self, request):
        service_response = EventService.get_events(owner=request.user)

        return paginate_response(
            service_response, serializers.GetEventSerializer, request
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
        participants = EventService.get_event_participants(
            user=request.user, event_id=pk
        )
        return paginate_response(participants, UserSerializer, request)

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

    @swagger_auto_schema(
        operation_description="List event tickets",
        operation_summary="List event tickets",
        tags=["Event-Admin"],
    )
    @action(detail=False, methods=["get"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/tickets")
    def list_tickets(self, request, pk):
        service_response = TicketService.list_event_tickets(pk)
        return Response(
            data=dict(
                event=serializers.TicketSerializer(service_response, many=True).data
            )
        )

    @swagger_auto_schema(
        operation_description="Admin send email to users",
        operation_summary="Admin send email to users",
        tags=["Event-Admin"],
    )
    @action(
        detail=False, methods=["post"], url_path="(?P<pk>[a-z,A-Z,0-9]+)/send-email"
    )
    def send_user_email(self, request, pk):
        serializer_ = serializers.SendEmailSerializer(data=request.data)
        serializer_.is_valid(raise_exception=True)

        return EventService.send_email_to_users(
            event_id=pk, user=request.user, **serializer_.data
        )

    @swagger_auto_schema(
        operation_description="Get single event detail",
        operation_summary="Get single event detail",
        tags=["Event"],
    )
    def retrieve(self, request, pk):
        service_response = EventService.get_single_event(id=pk)
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
            data=serializers.GetEventCategorySerializer(service_response).data
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

        return Response(data=dict(event_category=serializer))
