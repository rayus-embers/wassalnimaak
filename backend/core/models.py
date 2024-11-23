from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    is_adult = models.BooleanField(default=False)

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
    cartype = models.CharField(max_length=50,choices=CarType.choices(),default=CarType.SEDAN.name,)
    car_picture = models.ImageField(upload_to='car_pictures/', blank=True, null=True)
    driving_licence_picture = models.ImageField(upload_to='driving_licence_pictures/', blank=True, null=True)
    verified= models.BooleanField(default=False)
    banned=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    #resizing the image
    def save(self, *args, **kwargs):
    # Call the parent class's save method with all arguments
        super().save(*args, **kwargs)

    # Check if the pfp exists
        if self.profile_picture:
            try:
                pic = Image.open(self.profile_picture.path)

                if pic.height > 300:
                    output_size = (200, 90)
                    pic.thumbnail(output_size)
                    pic.save(self.profile_picture.path)
            except Exception as e:
                print(f"Error processing the image: {e}")
    