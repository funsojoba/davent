from django.urls import path, include

from .views import PaymentViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("", PaymentViewset, basename="payment")
urlpatterns = router.urls
