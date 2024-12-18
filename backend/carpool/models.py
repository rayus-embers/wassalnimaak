from django.db import models
from core.models import Driver,User

# Create your models here.

class Option(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Covoiturage(models.Model):
    departure_id = models.PositiveIntegerField()
    destination_id = models.PositiveIntegerField()
    addresses = models.JSONField(null = True, blank=True)
    time = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    options = models.ManyToManyField(Option, related_name='covoiturages', blank=True)
    price = models.FloatField()
    driver = models.ForeignKey(User, related_name="covoiturages", on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.departure_id} to {self.destination_id} - Driver: {self.driver.username}"



class Status(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    covoiturage = models.ForeignKey(Covoiturage, related_name="statuses", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    passenger = models.ForeignKey(User, related_name="statuses", on_delete=models.CASCADE)
    seats_reserved = models.PositiveIntegerField(default=1)  # Number of seats passenger wants to reserve
    confirmation_date = models.DateTimeField(null=True, blank=True)

    def cancel_pending_statuses(self):
        if self.covoiturage.available_seats == 0:
            Status.objects.filter(covoiturage=self.covoiturage, status='PENDING').update(status='CANCELLED')

    def save(self, *args, **kwargs):
        if self.status == 'CONFIRMED':
            # Handle confirmation date and seat reduction
            if self.confirmation_date is None:
                self.confirmation_date = models.DateTimeField(auto_now=True)

            if self.covoiturage.available_seats < self.seats_reserved:
                raise ValidationError(f"Only {self.covoiturage.available_seats} seats are available.")

            self.covoiturage.available_seats -= self.seats_reserved
            self.covoiturage.save()

            # Cancel pending statuses after confirming
            self.cancel_pending_statuses()

        super().save(*args, **kwargs)



class Payment(models.Model):
    payment_date = models.DateField(auto_now_add=True)  # Automatically set the date when created
    status = models.BooleanField(default=False)
    status_instance = models.ForeignKey('Status', on_delete=models.CASCADE, related_name="payments")

    def __str__(self):
        return f"Payment for Status {self.status_instance.id} - {'Completed' if self.status else 'Pending'}"

class Feedback(models.Model):
    rating = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_feedbacks")  # Passager
    about = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="received_feedbacks")  # Conducteur
    comment = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Feedback by {self.author.username} about {self.about.user.username} - Rating: {self.rating}"

