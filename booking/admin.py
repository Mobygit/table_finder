from django.contrib import admin
from .models import Table, MenuItem, Reservation

# Register your models here.

admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(Reservation)
