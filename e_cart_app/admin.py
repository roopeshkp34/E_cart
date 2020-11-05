from django.contrib import admin
from .models import Dealer,Customer,CustomUser,Product,Order,OrderItem
# Register your models here.

admin.site.register(Dealer)
admin.site.register(Customer)
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


