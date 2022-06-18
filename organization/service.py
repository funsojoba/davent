from rest_framework import status
from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Organization
from .serializers import OrganizationSerializer

from event.service import EventService


class OrganizationService:
    @classmethod
    def create_organization(cls, user, **kwargs):

        existing_record = Organization.objects.filter(name=kwargs.get("name")).first()
        if existing_record:
            return Response(
                errors={"error": "Organization with this name already exists"}
            )

        organization = Organization.objects.create(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            category=kwargs.get("category"),
            owner=user,
        )
        return Response(data=OrganizationSerializer(instance=organization).data)

    @classmethod
    def get_organization(cls, **kwargs):
        return Organization.objects.filter(**kwargs).first()

    @classmethod
    def list_organization(cls, **kwargs):
        return Organization.objects.filter(**kwargs)

    @classmethod
    def update_organization(cls, organization_id, **kwargs):
        organization = Organization.objects.filter(id=organization_id).first()
        organization.name = kwargs.get("name", "")
        organization.description = kwargs.get("description", "")
        organization.category = kwargs.get("category", "")
        organization.save()
        return organization

    @classmethod
    def get_events_by_organization(cls, org_id):
        organization = cls.get_organization(id=org_id)
        return EventService.get_events(organization=organization)
