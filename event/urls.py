from django.urls import path, include

from .views import UserEventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("", UserEventViewSet, basename="event")
urlpatterns = router.urls
