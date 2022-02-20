from django.urls import path, include
from .views import AuthViewSet, UserViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)


router.register("", AuthViewSet, basename="auth")
router.register("user", UserViewset, basename="user")
urlpatterns = router.urls
