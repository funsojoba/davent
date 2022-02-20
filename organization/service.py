from helpers.response import Response
from helpers.permissions import IsAdminUser, IsUser

from .models import Organization


class OrganizationService:
    @classmethod
    def create_organization(cls, **kwargs):
        return Organization.objects.create(**kwargs)
