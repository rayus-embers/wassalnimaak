from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Covoiturage, Status, Payment, Feedback
from .serializers import CovoiturageSerializer, StatusSerializer, PaymentSerializer, FeedbackSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerifiedDriver, IsCovoiturageOwner, IsStatusEditable
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Covoiturage
from .serializers import CovoiturageSerializer
# Create your views here.



class CovoiturageViewSet(ModelViewSet):
    queryset = Covoiturage.objects.all()
    serializer_class = CovoiturageSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['available_seats', 'price', 'options__id']
    search_fields = ['addresses']
    ordering_fields = ['price', 'available_seats']
    ordering = ['price']

    def get_permissions(self):
        """
        Use different permissions for different actions.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCovoiturageOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Automatically associate the logged-in verified driver with the covoiturage.
        """
        serializer.save(driver=self.request.user)


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsStatusEditable]

    def perform_update(self, serializer):
        """
        Additional validation to ensure only drivers can confirm or cancel, and passengers can cancel.
        """
        instance = self.get_object()
        user = self.request.user
        new_status = self.request.data.get('status')

        if user == instance.covoiturage.driver:
            if new_status in ['CONFIRMED', 'CANCELLED']:
                serializer.save()
                return

        # Only the passenger can cancel their request
        if user == instance.passenger and new_status == 'CANCELLED':
            serializer.save()
            return

        # If none of the above conditions are met, raise a permission error
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("You do not have permission to perform this action.")


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]


