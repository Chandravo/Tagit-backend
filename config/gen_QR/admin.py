from django.contrib import admin
from .models import QR, orders, Scan
# Register your models here.
admin.site.register(QR)
admin.site.register(orders)
admin.site.register(Scan)