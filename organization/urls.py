from django.urls import path, include

from .views import OrganizationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("", OrganizationViewSet, basename="organization")
urlpatterns = router.urls
