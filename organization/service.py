from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationService:
    @classmethod
    def create_organization(cls, user, **kwargs):
        organization = Organization.objects.create(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            category=kwargs.get("category"),
            owner=user,
        )
        return OrganizationSerializer(instance=organization).data

    @classmethod
    def get_organization(cls, **kwargs):
        return Organization.objects.filter(**kwargs).first()

    @classmethod
    def list_organization(cls, **kwargs):
        return Organization.objects.filter(**kwargs)
