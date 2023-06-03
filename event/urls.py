from django.urls import path, include

from .views import UserEventViewSet, EventCategoryViewSet, AdminEventViewSet
from .views import view_template
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("user", UserEventViewSet, basename="event_user")
router.register("admin", AdminEventViewSet, basename="event_admin")
router.register(r"category", EventCategoryViewSet, basename="event-category")
urlpatterns = router.urls


template_path = [path("template", view_template, name="template")]

urlpatterns + template_path
