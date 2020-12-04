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
import json
import datetime
from datetime import *



def dealer_login(request):
    try:
        if request.user.user_type == "2":
            return redirect("dealer_home")
    except:
        return render(request,"dealer_template/dealer_login.html")
    else:
        return render(request,"dealer_template/dealer_login.html")



def dealer_dologin(request):
    if request.user.is_authenticated:
        return redirect("dealer_home")
    elif request.method == 'POST':
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
        return render(request,'dealer_template/dealer_login.html')




# @user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def dealer_home(request):
    try:    
        user=request.user.id
        dealer=Dealer.objects.get(admin=user)
        products=Product.objects.filter(dealer_id=dealer).count()
        order_count=Order.objects.filter(dealer_id=dealer).count()


        # total price counting
        orders=Order.objects.filter(dealer_id=dealer)
        total = 0
        for order in orders:
            try:
                order_total=order.get_cart_total
            except:
                order_total=0
            total=total+order_total

        # total count of customers
        customer_count=Customer.objects.all().count()
        

        # chart
        year = datetime.now().year
        month = datetime.now().month
        chart_order = Order.objects.filter(date_ordered__year = year,date_ordered__month = month,dealer_id=dealer)
        

        chart_values = []
        
        for i in range(0,6):
            chart_order = Order.objects.filter(date_ordered__year = year,date_ordered__month = month-5+i)
            order_total = 0
            for items in chart_order:
                try:
                    order_total += round(items.get_cart_total,2)
                except:
                    order_total += 0
            chart_values.append(round(order_total,2)) 

        context = {
            "products":products,
            "order_count":order_count,
            "total":total,
            "customer_count":customer_count,
            "chart_values":chart_values,
        }
        return render(request,"dealer_template/dealer_home.html",context)
    except:
        return redirect("dealer_login")


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
    categorys = ProductCategory.objects.all()
    context = {
        "categorys":categorys,
    }
    return render(request,"dealer_template/add_product_template.html",context)




@user_passes_test(lambda u: u.user_type == '2',login_url='dealer_login')
def add_product_save(request):
    if request.method == 'POST':
        product_name=request.POST.get('product_name')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        category=request.POST.get('category')
        category_obj=ProductCategory.objects.get(id=category)
        # image_data =request.POST.get('image64data')
        dealer_id=Dealer.objects.get(admin=request.user.id)
        # value = image_data.strip('data:image/png;base64,')
        
        # format, imgstr = image_data.split(';base64,')
        # ext = format.split('/')[-1]

        # data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        product_image = request.FILES['image1']
        images = request.FILES.getlist('file[]')

        item = Product(product_name = product_name,dealer_id=dealer_id,price = price, quantity = quantity,category=category_obj, image = product_image)
        item.save()

        for image in images:
            fs=FileSystemStorage()
            file_path=fs.save(image.name,image)
            pimage=Product_images(product_id=item,product_image=file_path)
            pimage.save()
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
        product_image = request.FILES['image1']
        images = request.FILES.getlist('file[]')
        # image_data =request.POST.get('image64data')
        dealer_id=Dealer.objects.get(admin=request.user.id)
        # value = image_data.strip('data:image/png;base64,')
        
        # format, imgstr = image_data.split(';base64,')
        # ext = format.split('/')[-1]

        # data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
        
        item=Product.objects.get(id=product_id)
        item.product_name = product_name
        item.dealer_id=dealer_id
        item.price = price
        item.quantity = quantity
        item.category=category
        item.image = product_image
        item.save()
        for image in images:
            fs=FileSystemStorage()
            file_path=fs.save(image.name,image)
            pimage=Product_images(product_id=item,product_image=file_path)
            pimage.save()
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
    user=request.user.id
    dealer=Dealer.objects.get(admin=user)
    # print("dealer",dealer)
    orders = Order.objects.filter(dealer_id=dealer)
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



def add_offers(request):
    if request.method == "POST":
        offer_name=request.POST.get('offer_name')
        product=request.POST.get('product')
        discount_amount=request.POST.get('discount_amount')
        user=request.user.id
        dealer=Dealer.objects.get(admin=user)
        # dealer=request.POST.get('dealer')
        # print("offername",offer_name,"product",product,"dic",discount_amount)
        product_obj=Product.objects.get(id=product)

        ofer_exist=Offer.objects.filter(product=product_obj,dealer=dealer).exists()
        if ofer_exist:
            price=product_obj.offer_price
            discount_amounts= int(discount_amount)
            offers_price=price-(int(price)*(discount_amounts/100))

            offer = Offer.objects.get(product=product_obj,dealer=dealer)
            offer.discount_amount=discount_amount
            offer.offer_name=offer_name
            offer.save()
            product_obj.price=offers_price
            product_obj.save()
            
        else:
            offers=Offer.objects.create(offer_name=offer_name,discount_amount=discount_amount,product=product_obj,dealer=dealer)
            # offers.save()
            price=product_obj.price
            product_obj.offer_price=price
            discount_amounts= int(discount_amount)
            offer_price=price-(int(price)*(discount_amounts/100))
            product_obj.price=offer_price
            # product_obj.save()
        return redirect('manage_offers')

    else:
        dealer=Dealer.objects.get(admin=request.user.id)
        products=Product.objects.filter(dealer_id=dealer)
        context = {
            "products":products,
        }
        return render(request,"dealer_template/add_offer.html",context)


def manage_offers(request):
    user=request.user.id
    dealer=Dealer.objects.get(admin=user)
    offer=Offer.objects.filter(dealer=dealer)
    context = {
        "offers":offer,
    }
    return render(request,"dealer_template/manage_offers.html",context)


def add_category_offers(request):
    categorys = ProductCategory.objects.all()
    context = {
        "categorys":categorys
    }
    return render(request,"dealer_template/add_category_offers.html",context)


def add_category_offers_save(request):
    offer_name=request.POST.get('offer_name')
    categorys=request.POST.get('category')
    discount_amount=request.POST.get('discount_amount')

    dealer=Dealer.objects.get(admin=request.user.id)
    category_obj=ProductCategory.objects.get(id=categorys)
    products=Product.objects.filter(dealer_id=dealer,category=category_obj)

    for product in products:
        if product.offer_price == None:
            price=product.price
            discount_amounts= int(discount_amount)
            offers_price=price-(int(price)*(discount_amounts/100))
            # print(offer_price)
        else:
            price=product.offer_price
            discount_amounts= int(discount_amount)
            offers_price=price-(int(price)*(discount_amounts/100))
        

        ofer_exist=Offer.objects.filter(product=product,dealer=dealer).exists()
        if ofer_exist:
            offer = Offer.objects.get(product=product,dealer=dealer)
            # discount_amounts= int(discount_amount)
            # offers_price=int(product.offer_price)*(discount_amounts/100)
            offer.discount_amount=discount_amount
            offer.offer_name=offer_name
            offer.save()
            product.price=offers_price
            product.save()
        else:
            offer=Offer(offer_name=offer_name,discount_amount=discount_amount,product=product,dealer=dealer)
            offer.save()
            product.offer_price=price
            product.price=offers_price
            product.save()
    return redirect("add_category_offers")