from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models
from .models import User, Driver, CarType, Car

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import datetime

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','CIN','last_name','email', 'username','password','phone_number','birth_date','profile_picture',]
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        if validated_data.get('birth_date') is not None:
            today = datetime.date.today()

            birth_date = validated_data['birth_date']  

            min_age_date = today.replace(year=today.year - 18)

            if birth_date > min_age_date:  
                raise serializers.ValidationError({"birth_date": "You must be 18 or older to use WassalniMaak"})
            if validated_data.get('profile_picture') is not None:
                user = User.objects.create_user(
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    birth_date=birth_date,
                    CIN = validated_data['CIN'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    phone_number=validated_data['phone_number'],
                    profile_picture=validated_data['profile_picture'],
                    password = validated_data['password'],
                )
            else :
                user = User.objects.create_user(
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    birth_date=birth_date,
                    CIN = validated_data['CIN'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    phone_number=validated_data['phone_number'],
                    #profile_picture=validated_data['profile_picture'],
                    password = validated_data['password'],
                )
            return user
        else:
                raise serializers.ValidationError({"birth_date": "You must provide your birth date"})

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'birth_date')
        extra_kwargs = {
            'email': {'required': False},
            'phone_number': {'required': False},
        }
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RegisterDriverSerializer(serializers.ModelSerializer):
    driving_licence_picture = serializers.ImageField(required=False)

    class Meta:
        model = Driver
        fields = [
            "user",
            "bio",
            "driving_licence_picture",
        ]
        extra_kwargs = {
            'user':{'write_only': True},
        }
    def validate(self, attrs):
        """
        Custom validation if needed
        """
        if not self.instance and "user" not in attrs:
            raise serializers.ValidationError(
                {"user": "User must be provided when creating a driver."}
            )
        return attrs
    def create(self, validated_data):
        return Driver.objects.create(**validated_data)

    def update(self,instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

class DriverSerializer(serializers.ModelSerializer):
    person_username = serializers.CharField(source='driver.username', read_only=True)
    class Meta:
        model = Driver
        fields = [
            "user",
            "cartype",
            "car_picture",
            "driving_licence_picture",
            "verified",
            "banned",
        ]
    

class ChangePassowrdSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('old_password', 'password')


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'