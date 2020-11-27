from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from e_cart_app.models import *
from django.contrib.auth.decorators import user_passes_test
import base64
from PIL import Image
# from base64 import decodestring
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile



def admin_login(request):
    return render(request,'admin_template/admin_login.html')



def admin_dologin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                # return HttpResponse("hi")
                if user.user_type == "1":
                    return redirect("admin_home")
                else:
                    messages.error(request,'Invalid Login Details')
                    return HttpResponseRedirect("admin_login")
            else:
                messages.error(request,'Invalid Login Details')
                return HttpResponseRedirect("admin_login")
        except:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("admin_login")

    else:
        return render(request,'admin_template/admin_login.html')



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_home(request):
    product_count = Product.objects.all().count()
    order_count=Order.objects.all().count()
    dealer_count = Dealer.objects.all().count()

    # total price counting
    orders=Order.objects.all()
    total = 0
    for order in orders:
        try:
            order_total=order.get_cart_total
        except:
            order_total=0
        total=total+order_total

    context = {
        "product_count":product_count,
        "order_count":order_count,
        "total":total,
        "dealer_count":dealer_count,
    }
    return render(request,'admin_template/admin_home.html',context)


 

def admin_logout(request):
    logout(request)
    return redirect("admin_login")


@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def add_dealer(request):
    return render(request,'admin_template/add_dealer.html')




@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def save_add_dealer(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        address=request.POST.get('address')
        mobile_number=request.POST.get('mobile')
        image_data =request.POST.get('image64data')


        value = image_data.strip('data:image/png;base64,')
        
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)

        user=CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name,user_type=2)
        # dealer=Dealer.objects.get(id=user)
        user.dealer.address=address
        user.dealer.mobile_number=mobile_number
        user.dealer.image=data
        user.save()
        return redirect("/add_dealer")
    else:
        return redirect("/add_dealer")


    

@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def manage_dealer(request):
    dealers=Dealer.objects.all()
    context={
        "dealers":dealers,
    }
    return render(request,"admin_template/manage_dealer_template.html",context)



def view_dealer(request,dealer_id):
    dealers=Dealer.objects.get(id=dealer_id)
    context={
        "dealers":dealers,
    }
    return render(request,"admin_template/view_dealer.html",context)








 

@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def edit_dealer(request,dealer_id):
    dealer=Dealer.objects.get(admin=dealer_id)
    context= {
        "dealer":dealer,
    } 
    return render(request,"admin_template/edit_dealer_template.html",context)



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def save_edit_dealer(request):
    if request.method == 'POST':
        dealer_id=request.POST.get("dealer_id")
        first_name=request.POST.get('first_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        last_name=request.POST.get('last_name')
        address=request.POST.get('address')
        mobile_number=request.POST.get('mobile')
        image_data =request.POST.get('image64data')

        value = image_data.strip('data:image/png;base64,')
        
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)

        user=CustomUser.objects.get(id=dealer_id)
        user.first_name=first_name
        user.last_name=last_name
        user.username=username
        user.email=email
        user.save()

        dealer=Dealer.objects.get(admin=dealer_id)
        dealer.address=address
        dealer.mobile_number=mobile_number
        dealer.image = data
        dealer.save()

        return redirect("/edit_dealer/"+dealer_id)
    else:
        return render(request,"admin_template/edit_dealer_template.html")



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def delete_dealer(request,dealer_id):
    dealer=Dealer.objects.get(admin=dealer_id)
    dealer.delete()
    return redirect("manage_dealer")




@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_view_product(request):
    product=Product.objects.all()
    context={
        "product":product
    }
    return render(request,"admin_template/admin_view_product.html",context)




@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_edit_product(request,product_id):
    product=Product.objects.get(id=product_id)
    # print(product)
    context ={
        "product":product,
    }
    return render(request,"admin_template/edit_product.html",context)




@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def save_admin_edit_product(request):
    if request.method == 'POST':
        product_id=request.POST.get('product_id')
        product_name=request.POST.get('product_name')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        category=request.POST.get('category')
        image_data =request.POST.get('image64data')
        value = image_data.strip('data:image/png;base64,')
        
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        item=Product.objects.get(id=product_id)
        item.product_name = product_name
        item.price = price
        item.quantity = quantity
        item.category=category
        item.image = data
        item.save()
        return redirect("admin_view_product")
    else:
        return render(request,"admin_template/edit_product.html")



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_delete_product(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    return redirect("admin_view_product")



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_deactive(request,product_id):
    product=Product.objects.get(id=product_id)
    product.active=1
    product.save()
    return redirect("admin_view_product")



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_active(request,product_id):
    product=Product.objects.get(id=product_id)
    product.active=0
    product.save()
    return redirect("admin_view_product")
    



@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def admin_order_view(request):
    orders = Order.objects.all()
    # print(orders[0].customer
    context = {
        "orders":orders,
    }

    return render(request,"admin_template/admin_view_order.html",context)






@user_passes_test(lambda u: u.is_superuser,login_url='admin_login')
def manage_users(request):
    customer=CustomUser.objects.filter(user_type=3)
    context = {
        "customers":customer,
    }
    return render(request,"admin_template/manage_user_template.html",context)



def add_category(request):
    if request.method == 'POST':
        category_name=request.POST.get("category")
        ProductCategory.objects.create(category_name=category_name)
        return redirect("manage_category")
    else:
        return render(request,"admin_template/add_category.html")



def manage_category(request):
    category= ProductCategory.objects.all()
    context = {
        "categorys":category,
    }
    return render(request,"admin_template/manage_category.html",context)