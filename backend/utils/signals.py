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
def status_applied(sender, instance, created, **kwargs):
    if created and instance.status == 'PENDING':
        driver = instance.covoiturage.driver
        notification = Notification(
            user=driver.user,
            message=f"User {instance.passenger.username} has applied for your ride."
        )
        notification.save()

# Signal for when a user's status changes to 'CONFIRMED'
@receiver(post_save, sender=Status)
def status_confirmed(sender, instance, **kwargs):
    if instance.status == 'CONFIRMED':
        passenger = instance.passenger
        notification = Notification(
            user=passenger,
            message=f"Your ride has been confirmed!"
        )
        notification.save()
