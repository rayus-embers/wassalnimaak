# utils/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from carpool.models import Feedback, Status 
from core.models import User  
from .models import Notification  

# Signal for when a feedback is posted about a driver
@receiver(post_save, sender=Feedback)
def feedback_posted(sender, instance, created, **kwargs):
    if created:
        driver = instance.about
        notification = Notification(
            user=driver.user,
            message=f"You have received a new feedback from {instance.author.username}."
        )
        notification.save()

# Signal for when a user applies for a ride
@receiver(post_save, sender=Status)
def handle_status_change(sender, instance, created, **kwargs):
    # Notify driver when a new pending application is created
    if created and instance.status == 'PENDING':
        driver = instance.covoiturage.driver
        Notification.objects.create(
            user=driver,
            message=f"User {instance.passenger.username} has applied for your ride for {instance.seats_reserved} seats."
        )
    
    # Notify passenger when status changes to 'CONFIRMED'
    elif instance.status == 'CONFIRMED':
        passenger = instance.passenger
        Notification.objects.create(
            user=passenger,
            message=f"Your ride with {instance.driver.user.username} has been confirmed!"
        )

