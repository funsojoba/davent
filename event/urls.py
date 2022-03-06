from django.urls import path, include

from .views import UserEventViewSet, EventCategoryViewSet, AdminEventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("user", UserEventViewSet, basename="event_user")
router.register("", AdminEventViewSet, basename="event")
router.register(r"category", EventCategoryViewSet, basename="event-category")
urlpatterns = router.urls
