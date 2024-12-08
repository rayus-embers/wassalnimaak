from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum
from PIL import Image
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    CIN = models.CharField(max_length=8, blank=True, null=True, unique=True)

    def __str__(self):
        return self.username



class CarType(Enum):
    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    CONVERTIBLE = "Convertible"
    COUPE = "Coupe"
    WAGON = "Wagon"
    PICKUP = "Pickup"
    MINIVAN = "Minivan"
    SPORTS = "Sports Car"
    ELECTRIC = "Electric Car"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="driver")
    rating = models.FloatField(default=0)
    bio = models.TextField(max_length=500, null=True, blank=True, default="This driver didn't add a bio")
    driving_licence_picture = models.ImageField(upload_to='driving_licence_pictures/', blank=True, null=True)
    verified= models.BooleanField(default=False)
    banned=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
    #resizing the image
    def save(self, *args, **kwargs):
    # Call the parent class's save method with all arguments
        super().save(*args, **kwargs)

    # Check if the pfp exists
        if self.driving_licence_picture:
            try:
                pic = Image.open(self.driving_licence_picture.path)

                if pic.height > 300:
                    output_size = (200, 90)
                    pic.thumbnail(output_size)
                    pic.save(self.driving_licence_picture.path)
            except Exception as e:
                print(f"Error processing the image: {e}")
    

class Car(models.Model):
    driver = models.ForeignKey(Driver, related_name="cars", on_delete=models.CASCADE)
    make = models.CharField(max_length=100)  
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    cartype = models.CharField(max_length=50,choices=CarType.choices(),default=CarType.SEDAN.name,)
    car_picture = models.ImageField(upload_to='car_pictures/', blank=True, null=True)
    license_plate = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
    # Call the parent class's save method with all arguments
        super().save(*args, **kwargs)

    # Check if the pfp exists
        if self.car_picture:
            try:
                pic = Image.open(self.car_picture.path)

                if pic.height > 300:
                    output_size = (200, 90)
                    pic.thumbnail(output_size)
                    pic.save(self.car_picture.path)
            except Exception as e:
                print(f"Error processing the image: {e}")
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - {self.license_plate}"