from django.contrib import admin
from .models import Product,ProductCategory,Reservation,Order
# Register your models here.


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Reservation)
admin.site.register(Order)