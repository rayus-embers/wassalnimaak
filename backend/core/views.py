from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User, Driver, Car
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CarSerializer, RegisterSerializer, UserSerializer, RegisterDriverSerializer, DriverSerializer, ChangePassowrdSerializer, UserProfileSerializer
# Create your views here.
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return your username, user id
        """
        return Response({
            "username":request.user.username,
            "id":request.user.pk,
        })

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "User created successfully and logged in.",
        })

class UserProfileUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully!",
                "user": serializer.data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterDriverApi(generics.GenericAPIView):
    serializer_class = RegisterDriverSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args,  **kwargs):
        print(request.user.pk==request.data['user'])
        #verify if the user is truly the one tryna make a driver account
        if request.user.pk==request.data['user']:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            driver = serializer.save()
            return Response({
                "message": "Driver Created Successfully."
            })
        else :
            return Response({
            "message":"tryna be sneaky ey?"
        })
    def put(self, request, *args, **kwargs):
        try:
            instance = Driver.objects.get(pk=request.data['user'])
        except Driver.DoesNotExist:
            return Response({
                "message": "Driver not found."
            })

        if f'{request.user.pk}' == str(instance.user.pk):
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            driver = serializer.save()
            return Response({
                "message": "Driver updated.",
            })
        else:
            return Response({
                "message": "Trying to be sneaky, ey?"
            },)
    
    def patch(self, request, *args, **kwargs):
        try:
            instance = Driver.objects.get(pk=request.data['id'])
        except Driver.DoesNotExist:
            return Response({
                "message": "Driver not found."
            })

        if f'{request.user.pk}' == str(instance.user.pk):
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            driver = serializer.save()
            return Response({
                "message": "Driver partially updated.",
            })
        else:
            return Response({
                "message": "Trying to be sneaky, ey?"
            })

class ChangePasswordAPI(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePassowrdSerializer
    def put(self, request, *args, **kwargs):
        try:
            user = request.user
        except user.DoesNotExist:
            #better be safe than sorry
            return Response({
                "message": "user not found."
            })

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "password updated.",
        })
    

class DriverDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            driver = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            raise NotFound({"detail": "Driver not found."})

        car_picture_url = (
            driver.car_picture.url if driver.car_picture else "/media/default_car.jpg"
        )

        driving_licence_picture_url = (
            driver.driving_licence_picture.url
            if driver.driving_licence_picture
            else "/media/default_driving_licence.jpg"
        )

        return Response({
            "username": driver.user.username,
            "rating": driver.rating,
            "car_type": driver.cartype,
            "verified": driver.verified,
            "banned": driver.banned,
            "car_picture": car_picture_url,
            "driving_licence_picture": driving_licence_picture_url,
        })

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow drivers to only see their own cars
        user = self.request.user
        if hasattr(user, 'driver'):
            return self.queryset.filter(driver=user.driver)
        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'driver'):
            serializer.save(driver=user.driver)
        else:
            raise serializers.ValidationError("You must be a driver to add a car.")