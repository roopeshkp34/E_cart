from django.contrib import admin
from .models import Dealer,Customer,CustomUser
# Register your models here.

admin.site.register(Dealer)
admin.site.register(Customer)
admin.site.register(CustomUser)