from rest_framework.permissions import BasePermission

class IsVerifiedDriver(BasePermission):
    """
    Custom permission to only allow verified drivers to create "covoiturages".
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'driver') :
            return request.user.driver.verified
        return False

class IsCovoiturageOwner(BasePermission):
    """
    Custom permission to only allow the driver who created the covoiturage to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.driver
    
class IsStatusEditable(BasePermission):
    """
    Custom permission to allow only the driver or the passenger to update the status.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if the user is the driver of the associated covoiturage
        if user == obj.covoiturage.driver:
            return True

        # Check if the user is the passenger of the status
        if user == obj.passenger:
            return request.method in ['PATCH', 'PUT', 'GET']

        return False