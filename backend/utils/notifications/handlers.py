from utils.models import Notification

def notify_driver(driver, passenger, ride):
    """
    Notify the driver when a passenger requests to join their ride.
    """
    title = "New Ride Request"
    message = f"{passenger.username} has requested to join your ride from {ride.departure_id} to {ride.destination_id}."
    Notification.objects.create(user=driver.user, title=title, message=message)

def notify_passenger(passenger, driver, ride):
    """
    Notify the passenger when the driver accepts their ride request.
    """
    title = "Request Accepted"
    message = f"{driver.user.username} has accepted your request for the ride from {ride.departure_id} to {ride.destination_id}."
    Notification.objects.create(user=passenger, title=title, message=message)

def notify_passengers(passengers, driver, ride):
    """
    Notify all passengers when the driver is almost ready to depart.
    """
    for passenger in passengers:
        title = "Driver is on the Way"
        message = f"{driver.user.username} is almost ready to depart for the ride from {ride.departure_id} to {ride.destination_id}."
        Notification.objects.create(user=passenger, title=title, message=message)
