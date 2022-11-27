from django.urls import path, include

from .views import PaymentViewset, AdminPaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("", PaymentViewset, basename="payment")
router.register("admin", AdminPaymentViewSet, basename="admin-payment")

urlpatterns = router.urls
