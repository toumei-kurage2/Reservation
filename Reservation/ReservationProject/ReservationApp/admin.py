from django.contrib import admin
from .models import Reservation,Reservation_detail,Account
# Register your models here.
admin.site.register(Reservation)
admin.site.register(Reservation_detail)
admin.site.register(Account)
