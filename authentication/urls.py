from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)


router.register("auth", UserViewSet, basename="auth")
# urlpatterns = [path("", include(router.urls))]
urlpatterns = router.urls
