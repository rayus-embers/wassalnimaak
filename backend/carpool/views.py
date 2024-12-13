from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from .models import Covoiturage, Status, Payment, Feedback
from .serializers import CovoiturageSerializer, StatusSerializer, PaymentSerializer, FeedbackSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsVerifiedDriver, IsCovoiturageOwner, IsStatusEditable
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Driver
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
    ordering_fields = ['price', 'available_seats', 'time']
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

    def get_queryset(self):
        """
        Filter feedbacks for a specific driver if the 'driver_id' query parameter is provided.
        Otherwise, return all feedbacks.
        """
        driver_id = self.request.query_params.get('driver_id', None)
        if driver_id:
            return Feedback.objects.filter(about_id=driver_id)
        return super().get_queryset()

    def perform_create(self, serializer):
        about = serializer.validated_data.get('about')
        print(type(about))

        # Ensure the 'about' user is valid (e.g., is a Driver).
        if not isinstance(about, Driver):
            raise ValidationError("The user you're reviewing must be a driver.")

        # Save feedback
        serializer.save(author=self.request.user)


