from django.contrib import admin
from .models import *

# Register your models here.

admin.register(Client)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Supply)
admin.site.register(SupplyBook)
admin.site.register(SupplyRequest)
admin.site.register(DeliveryRequest)
admin.site.register(Purchase)
