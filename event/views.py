from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response

from .server import EventService
from . import serializers


class UserEventViewSet(viewsets.ViewSet):
    permission_classes = (IsUser,)
    @swagger_auto_schema(
        operation_description="List organizations",
        operation_summary="List organizations",
        tags=["Event"],
    )
    @action(detail=False, method=["get"], url_path="list")
    def list_events(self, request):
        service_response = EventService.get_events()
        return Response(serializers.GetEventCategorySerializer(service_response, many=True).data)