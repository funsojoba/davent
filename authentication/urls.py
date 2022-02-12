from django.urls import path, include
from .views import AuthViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)


router.register("", AuthViewSet, basename="auth")
urlpatterns = router.urls
