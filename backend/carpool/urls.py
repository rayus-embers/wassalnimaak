from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CovoiturageViewSet, StatusViewSet, PaymentViewSet, FeedbackViewSet

router = DefaultRouter()
router.register(r'covoiturages', CovoiturageViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]