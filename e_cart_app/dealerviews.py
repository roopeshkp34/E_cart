from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from e_cart_app.models import *
from django.contrib.auth.decorators import user_passes_test
import base64
from PIL import Image
from base64 import decodestring
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
import json


def dealer_login(request):
    return render(request,"dealer_template/dealer_login.html")



def dealer_dologin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                # return HttpResponse("hi")
                if user.user_type == "2":
                    return redirect("dealer_home")
                else:
                    messages.error(request,'Invalid Login Details')
                    return HttpResponseRedirect("dealer_login")
            else:
                messages.error(request,'Invalid Login Details')
                return HttpResponseRedirect("dealer_login")
        except:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("dealer_login")

    else:
        return render(request,'admin_template/dealer_login.html')




@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def dealer_home(request):
    return render(request,"dealer_template/dealer_home.html")


def dealer_logout(request):
    logout(request)
    return redirect("dealer_login")



    

@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def manage_product(request):
    dealer=Dealer.objects.get(admin=request.user.id)
    products=Product.objects.filter(dealer_id=dealer)
    context = {
        "products":products,
    }
    return render(request,"dealer_template/manage_product.html",context)




@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def add_product(request):
    
    return render(request,"dealer_template/add_product_template.html")




@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def add_product_save(request):
    if request.method == 'POST':
        product_name=request.POST.get('product_name')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        category=request.POST.get('category')
        image_data =request.POST.get('image64data')
        dealer_id=Dealer.objects.get(admin=request.user.id)
        value = image_data.strip('data:image/png;base64,')
        
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)

        item = Product(product_name = product_name,dealer_id=dealer_id,price = price, quantity = quantity,category=category, image = data)
        item.save()
        return redirect("add_product")

    else:
        return render(request,"dealer_template/add_product_template.html")





@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def edit_product(request,product_id):
    product=Product.objects.get(id=product_id)
    # print(product)
    context ={
        "product":product,
    }
    return render(request,"dealer_template/edit_product.html",context)




@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def save_edit_product(request):
    if request.method == 'POST':
        product_id=request.POST.get('product_id')
        product_name=request.POST.get('product_name')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        category=request.POST.get('category')
        image_data =request.POST.get('image64data')
        dealer_id=Dealer.objects.get(admin=request.user.id)
        value = image_data.strip('data:image/png;base64,')
        
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        item=Product.objects.get(id=product_id)
        item.product_name = product_name
        item.dealer_id=dealer_id
        item.price = price
        item.quantity = quantity
        item.category=category
        item.image = data
        item.save()
        return redirect("manage_product")
    else:
        return render(request,"dealer_template/edit_product.html")





@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def delete_product(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    return redirect("manage_product")



@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def dealer_order_view(request):
    orders = Order.objects.all()
    # print(orders[0].customer)
    context = {
        "orders":orders,
    }

    return render(request,"dealer_template/dealer_view_order.html",context)




def update_order(request):
    data = json.loads(request.body)
    # print(data)
    orderId=data['orderId']
    status=data['status']

    # print(status)

    order = Order.objects.get(id = orderId)
    order.order_status = status
    order.save()

    return redirect('dealer_order_view')


    