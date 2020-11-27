from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1,"MD"),(2,"Dealer"),(3,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    refferal_code = models.CharField(max_length= 200, null = True)
    reffered_user = models.CharField(max_length= 200, null = True)
 


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
    image= models.ImageField(null = True, blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200,null = True)
    email = models.CharField(max_length= 200, null = True)
    
    # def __str__(self):
    #     return self.name




class ProductCategory(models.Model):
    category_name=models.CharField(max_length = 200,null = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)



class Product(models.Model):
    dealer_id=models.ForeignKey(Dealer,on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 200,null = True)
    price = models.FloatField()
    offer_price = models.FloatField(null=True)
    category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE,null = True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    active=models.IntegerField(default=0,null=True,blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null = True, blank = True,upload_to='product/images')

    def __str__(self):
        return self.product_name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Product_images(models.Model):
    id=models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_image = models.FileField(max_length=2555,upload_to='product/images')

    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url



class Offer(models.Model):
    offer_name = models.CharField(max_length= 220, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE,null=True)
    discount_amount = models.FloatField(null=True)
    offer_start = models.DateField(auto_now_add=True, null=True)
    offer_expiry = models.DateField(null=True)





class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank= True, null=True)
    dealer_id = models.ForeignKey(Dealer, on_delete=models.SET_NULL,blank= True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True,blank=False)
    transaction_id = models.CharField(max_length = 200, null = True )
    order_status = models.CharField(default = 'Pending',max_length = 200, null = True )

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self): 
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property   
    def get_total(self):
        try:
            total = self.product.price * self.quantity
        except:
            total = 0
        return total


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank= True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null = True)
    address = models.CharField(max_length = 200,null = True)
    city = models.CharField(max_length = 200,null = True)
    state = models.CharField(max_length = 200,null = True)
    zipcode = models.CharField(max_length = 200,null = True)
    country = models.CharField(max_length = 200,null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminMD.objects.create(admin = instance)
        if instance.user_type==2:
            Dealer.objects.create(admin = instance)
        if instance.user_type==3:
            Customer.objects.create(user = instance)




@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminmd.save()
    if instance.user_type==2:
        instance.dealer.save()
    if instance.user_type==3:
        instance.customer.save()