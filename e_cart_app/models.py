from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1,"MD"),(2,"Dealer"),(3,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class AdminMD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=models.Manager()


class Dealer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address=models.CharField(max_length = 200,null = True)
    mobile_number=models.CharField(max_length=13, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address=models.CharField(max_length = 200,null = True)
    mobile_number=models.CharField(max_length=13, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    dealer_id=models.ForeignKey(Dealer,on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 200,null = True)
    price = models.FloatField()
    category=models.CharField(max_length = 200,null = True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.product_name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminMD.objects.create(admin = instance)
        if instance.user_type==2:
            Dealer.objects.create(admin = instance)
        if instance.user_type==3:
            Customer.objects.create(admin = instance)




@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminmd.save()
    if instance.user_type==2:
        instance.dealer.save()
    if instance.user_type==3:
        instance.customer.save()