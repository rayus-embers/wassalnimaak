from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet
from .models import Covoiturage, Status, Payment, Feedback
from rest_framework.response import Response
from .serializers import CovoiturageSerializer, StatusSerializer, PaymentSerializer, FeedbackSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import IsVerifiedDriver, IsCovoiturageOwner, IsStatusEditable
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Driver
from rest_framework.exceptions import PermissionDenied
from .models import Covoiturage
from .serializers import CovoiturageSerializer
# Create your views here.



class CovoiturageFilter(filters.FilterSet):
    price = filters.NumberFilter(field_name="price", lookup_expr='lt')  # 'lt' for less than
    available_seats = filters.NumberFilter(field_name="available_seats", lookup_expr='gt')  # 'gt' for greater than
    driver = filters.NumberFilter(field_name='driver__id')
    class Meta:
        model = Covoiturage
        fields = ['price', 'available_seats', 'destination_id', 'departure_id', 'options__id', 'driver']

class CovoiturageViewSet(ModelViewSet):
    queryset = Covoiturage.objects.all()
    serializer_class = CovoiturageSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CovoiturageFilter  # Use the custom filter class
    search_fields = ['addresses']
    ordering_fields = ['price', 'available_seats', 'time']
    ordering = ['price']

    def get_permissions(self):
        try:
            if self.action in ['update', 'partial_update', 'destroy']:
                return [IsAuthenticated(), IsCovoiturageOwner()]
            return [IsAuthenticated()]
        except Exception as e:
            return Response({"error": f"Permission setup failed: {str(e)}"}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        try:
            serializer.save(driver=self.request.user)
        except Exception as e:
            raise ValidationError({"error": f"Failed to create covoiturage: {str(e)}"})



class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsStatusEditable]

    def perform_create(self, serializer):
        try:
            user = self.request.user
            covoiturage = serializer.validated_data['covoiturage']
            seats_reserved = serializer.validated_data.get('seats_reserved', 1)

            # Validate reservation
            if seats_reserved <= 0:
                raise ValidationError("You must reserve at least one seat.")
            if covoiturage.available_seats < seats_reserved:
                raise ValidationError(f"Only {covoiturage.available_seats} seats are available.")

            serializer.save(passenger=user)

        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {"error": f"Failed to create status: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            user = self.request.user
            new_status = self.request.data.get('status')
            new_seats_reserved = self.request.data.get('seats_reserved', instance.seats_reserved)

            if user == instance.covoiturage.driver:
                if new_status == 'CONFIRMED':
                    if instance.covoiturage.available_seats < new_seats_reserved:
                        raise ValidationError(f"Only {instance.covoiturage.available_seats} seats are available.")

                    # Reduce available seats only on confirmation
                    instance.covoiturage.available_seats -= new_seats_reserved
                    instance.covoiturage.save()

                    # Automatically cancel pending statuses if seats are zero
                    if instance.covoiturage.available_seats == 0:
                        Status.objects.filter(covoiturage=instance.covoiturage, status='PENDING').update(status='CANCELLED')

                if new_status in ['CONFIRMED', 'CANCELLED']:
                    serializer.save()
                    return

            if user == instance.passenger:
                if new_status == 'CANCELLED':
                    serializer.save()
                    return

            raise PermissionDenied("You do not have permission to perform this action.")
        except ValidationError as e:
            raise e
        except Exception as e:
            return Response(
                {"error": f"Failed to update status: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )



class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": f"Payment creation failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            driver_id = self.request.query_params.get('driver_id', None)
            if driver_id:
                return Feedback.objects.filter(about_id=driver_id)
            return super().get_queryset()
        except Exception as e:
            return Response({"error": f"Failed to fetch feedbacks: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:
            about = serializer.validated_data.get('about')

            if not isinstance(about, Driver):
                raise ValidationError("The user you're reviewing must be a driver.")

            serializer.save(author=self.request.user)
        except ValidationError as ve:
            raise ve
        except Exception as e:
            return Response(
                {"error": f"Feedback creation failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
