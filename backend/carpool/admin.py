from django.contrib import admin
from .models import Covoiturage,Status,Payment,Feedback,Option
# Register your models here.
admin.site.register(Covoiturage)
admin.site.register(Status)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(Option)