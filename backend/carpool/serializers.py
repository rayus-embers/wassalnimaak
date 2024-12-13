from rest_framework import serializers
from .models import Covoiturage, Status, Payment, Feedback, Option

class CovoiturageSerializer(serializers.ModelSerializer):
    options = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Option.objects.all()
    )

    class Meta:
        model = Covoiturage
        fields = ['id', 'departure_id', 'time', 'destination_id', 'addresses', 'available_seats', 'options', 'price', 'driver']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['author']
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
