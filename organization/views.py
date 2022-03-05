from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action

from helpers.permissions import IsAdminUser, IsUser
from helpers.response import Response

from .serializers import OrganizationSerializer, CreateOrganizationSerializer
from .service import OrganizationService


class OrganizationViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="List organizations",
        operation_summary="List organizations",
        tags=["Organization"],
        # responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["get"], url_path="list")
    def list_organization(self, request):
        service_response = OrganizationService.list_organization(owner=request.user)
        serializer = OrganizationSerializer(service_response, many=True)
        return Response(data=dict(data=serializer.data))

    @swagger_auto_schema(
        operation_description="Create organizations",
        operation_summary="Create organizations",
        tags=["Organization"],
        # responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_organization(self, request):
        serializer = CreateOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response = OrganizationService.create_organization(
            request.user, **serializer.data
        )
        return service_response

    @swagger_auto_schema(
        operation_description="Retrieve Organization",
        operation_summary="Retrieve Organization",
        tags=["Organization"],
        # responses=schema_example.COMPLETE_REGISTRATION_RESPONSES,
    )
    def retrieve(self, request, pk=None):
        service_response = OrganizationService.get_organization(pk)
        return Response(OrganizationSerializer(service_response).data)


    @swagger_auto_schema(
        operation_description="Update Organization Information",
        operation_summary="Update Organization Information", 
        tags=["Organization"]
    )
    def update(self, request, pk=None):
        service_response = OrganizationService.update_organization(pk)
        serializer = self.serializer_class(service_response, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "success"}, status=status.HTTP_200_OK)
            
        return Response(errors={"message": "Failure"}, status=status.HTTP_400_BAD_REQUEST)
