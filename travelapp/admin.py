from django.contrib import admin

# Register your models here.
from.models import *
admin.site.register(userLogin)
admin.site.register(Booking)
admin.site.register(Reservation)
admin.site.register(Hotel)
admin.site.register(HotelConfirm)
admin.site.register(CarView)
admin.site.register(CarBook)
