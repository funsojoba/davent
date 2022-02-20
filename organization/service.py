from rest_framework import status
from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Organization
from .serializers import OrganizationSerializer


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
    def get_organization(cls, id):
        return Organization.objects.filter(id=id).first()

    @classmethod
    def list_organization(cls, **kwargs):
        return Organization.objects.filter(**kwargs)
