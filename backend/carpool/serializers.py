from rest_framework import serializers
from .models import Covoiturage, Status, Payment, Feedback, Option
from core.models import Driver, User


class CovoiturageSerializer(serializers.ModelSerializer):
    # Define a nested serializer for the driver to fetch 'username' and 'profile_picture' from the User model
    class DriverSerializer(serializers.ModelSerializer):
        username = serializers.CharField()  # Fetching username from the related 'user' field
        profile_picture = serializers.ImageField()  # Fetching profile picture from the related 'user' field

        class Meta:
            model = Driver
            fields = ['username', 'profile_picture','pk']

    options = serializers.PrimaryKeyRelatedField(many=True, queryset=Option.objects.all(), required= False)
    addresses= serializers.JSONField(required= False)
    driver = DriverSerializer(read_only=True)  # Ensure it's read-only if you're not updating driver directly in this serializer

    class Meta:
        model = Covoiturage
        fields = [
            'id', 
            'departure_id', 
            'time', 
            'destination_id', 
            'addresses', 
            'available_seats', 
            'options', 
            'price', 
            'driver'  # The 'driver' field now contains username and profile_picture
        ]



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'covoiturage', 'status', 'seats_reserved', 'confirmation_date', 'passenger']
        read_only_fields = ['confirmation_date', 'passenger']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        username = serializers.CharField()  # Fetching username from the related 'user' field
        profile_picture = serializers.ImageField()  # Fetching profile picture from the related 'user' field

        class Meta:
            model = User
            fields = ['username', 'profile_picture']
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['author']
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
