from django.urls import path
from .views import Home, RegisterApi, RegisterDriverApi,ChangePasswordAPI, DriverDetail, UserProfileUpdateApi, CarViewSet
urlpatterns = [
    path('getmyid/', Home.as_view(), name="get the id"),
    path('register/', RegisterApi.as_view(), name="register user"),
    path('registerdriver/', RegisterDriverApi.as_view(), name="register Driver"),
    path('registerdriver/update/', RegisterDriverApi.as_view(), name="update Driver"),
    path('changepass/', ChangePasswordAPI.as_view(), name="change password"),
    path('read/driver/<int:pk>/', DriverDetail.as_view(), name="show Driver"),
    path('profile/update/', UserProfileUpdateApi.as_view(), name='profile-update'),
    #path('car', CarViewSet.as_view(), name='profile-update'),
]
