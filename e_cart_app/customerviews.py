from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from e_cart_app.models import *
import json
import datetime
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
import requests
import razorpay
from django.views.generic import View






def mobile(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        print(mobile)
        responce = redirect('otp')
        responce.set_cookie('mobile', mobile)
        return responce

    return render(request, 'user_template/mobile.html')


def otp(request):
    if request.method == 'GET':
        phone = request.COOKIES['mobile']
        print(phone)
        user = CustomUser.objects.filter(last_name = phone).exists()
        print(user)
        if not user:
            messages.info(request,'The mobile number is not registered')
            return redirect('mobile')
            
        url = "https://d7networks.com/api/verifier/send"
        num = str(91)+phone


        payload = {'mobile': num,
        'sender_id': 'SMSINFO',
        'message': 'Your otp code is {code}',
        'expiry': '900'}
        files = [

        ]
        headers = {
        'Authorization': 'Token 51fcb7ecb743790e4299f267497ee164496621bd'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))


        otp_id = response.text[11:47] 
        print(otp_id)                                                          
        responce  = render(request, 'user_template/otp.html')
        responce.set_cookie('otp_id', otp_id)
        return responce

    else:

        otp = request.POST.get('otp')
        print(otp)

        otp_id = request.COOKIES['otp_id']

        url = "https://d7networks.com/api/verifier/resend"

        payload = {'otp_id': otp_id,
        'otp_code': otp
        }
        files = [

        ]
        headers = {
        'Authorization': 'Token 51fcb7ecb743790e4299f267497ee164496621bd'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)


        b = json.loads(response.text)
        try:
            print(b["status"])
        except:
            b["status"] = 'failed'
            print(b["status"])
        if (b["status"] == "open"):
            phone = request.COOKIES['mobile']
            user = CustomUser.objects.get(last_name = phone )
            print(user)
            username = user.username
            password = user.first_name
            print(password)
            print(username)
            user = auth.authenticate(request, username = username, password = password)
            print(user)
            if user is not None:
                auth.login(request,user)
                print('login request')
                return redirect('/')
            else:
                messages.info(request, 'OTP did not match')
                return redirect('mobile')
        print(response.text.encode('utf8'))
        messages.info(request, 'OTP did not match')
        return redirect('mobile')



def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=auth.authenticate(username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                # return HttpResponse("hi")
                if user.user_type == "3":
                    return redirect("/")
                else:
                    messages.error(request,'Invalid Login Details')
                    return HttpResponseRedirect("/")
            else:
                messages.error(request,'Invalid Login Details')
                return HttpResponseRedirect("/")
        except:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("/")
    else:
        return render(request,'user_template/user_home.html')


def user_logout(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        mobile_number= request.POST.get('mobile_number')

        user = CustomUser.objects.create_user(username = username, password = password, email = email,first_name=password,last_name=mobile_number,user_type=3)
        # user.customer.mobile_number=mobile_number
        user.save()
        return redirect("/")

    else:
        return render(request,'user_template/user_signup.html')





def user__home(request):
    if request.user.is_superuser:
        admin=request.user
        order, created = Order.objects.get_or_create(customer=admin,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        return redirect('admin_home')
    # elif CustomUser.user_type == 2:
    #     admin=request.user
    #     order, created = Order.objects.get_or_create(customer=admin,complete=False)
    #     items=order.orderitem_set.all()
    #     cartItems=order.get_cart_items
    #     return redirect('dealer_login')
    elif request.user.is_authenticated:
        login_user = request.user
        login_name = request.user.username
        login_email = request.user.email
        user, created = Customer.objects.get_or_create(user = login_user, name = login_name, email = login_email)
        # print(login_user)
        # print(login_name)
        # print(login_email)
        customer=request.user.customer
        # print(customer)
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0, 'shipping':False}
        cartItems=order['get_cart_items']
    products=Product.objects.all()
    offer=Offer.objects.all()
    context= {
        "items":items,
        "products":products,
        "cartItems":cartItems,
        "offers":offer,
    }
    return render(request,"user_template/user_home.html",context)


def user_view_product(request,product_id):
    product=Product.objects.get(id=product_id)
    product_images = Product_images.objects.filter(product_id=product)
    print(product_images)
    if request.user.is_authenticated:
        admin=request.user.customer
        order, created = Order.objects.get_or_create(customer=admin,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    context ={
        "items":items,
        "product":product,
        "cartItems":cartItems,
        "product_images":product_images,
    }
    return render(request,"user_template/user_view_product.html",context)



def user_cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    context ={
        "items":items,
        "order":order,
        "cartItems":cartItems,
    }
    return render(request,"user_template/user_cart.html",context)



def user_checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        print(items)
        ship = ShippingAdress.objects.filter(customer=customer).distinct()

    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    client  = razorpay.Client(auth=("rzp_test_60LoLFkXcaDMVN", "sAlIyuylw1Ox8h7ryZVy7Y1c"))

    if request.user.is_authenticated:
        total = int(order.get_cart_total*100)
    else:
        total = int(order['get_cart_total']*100)
    print(total)
    order_amount = total
    order_currency = 'USD'
    order_receipt = 'order_rcptid_11'
    if order_amount == 0:
        return redirect('user_cart')
    else:


        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt,payment_capture = 0) )
        order_id = response['id']
        order_status = response['status']
        context ={
            "items":items,
            "order":order,
            "cartItems":cartItems,
            'order_id':order_id,
            "shipping":ship,

        }
    
        return render(request,"user_template/check_out.html",context)



class Getshipping(View):
    def get(self, request):
        text = request.GET.get('ship_id')
        print(text)

        shipi = ShippingAdress.objects.get(id=text)

        a = shipi.address
        b = shipi.city
        vb = {
            'address': shipi.address,
            'city': shipi.city,
            'state': shipi.state,
            'zipcode': shipi.zipcode,

        }
        return JsonResponse({'count2': vb}, status=200)
        return redirect('/')





def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("Action:", action)
    print("ProductId:", productId)

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    dealer=product.dealer_id
    print("dealer",dealer)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    order.dealer_id=dealer
    order.save()
    
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()
    


    return JsonResponse('Item was added' , safe=False) 




def processOrder(request):
    # print("Data",request.body)
    transaction_id=datetime.datetime.now().timestamp()
    data =json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        total= float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        print(order.shipping)
        if order.shipping == True:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
            # print(ShippingAdress.address)

    else:
        print("user is not loged in")
    return JsonResponse('Payment complete' , safe=False) 




def user_view_orders(request):
    try:
        customer=request.user.customer
        print(customer)
        order=Order.objects.filter(customer=customer,complete=True)
        items =[]
        for i in order:
            details=OrderItem.objects.filter(order=i,product__isnull=False)
            for j in details:
                items.append(j)

        if request.user.is_authenticated:
            customer=request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,complete=False)
            # items=order.orderitem_set.all()
            cartItems=order.get_cart_items

        else:
            # items=[]
            order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
            cartItems=order['get_cart_items']
    except:
        return redirect("/")
    context ={
        "items":items,
        "order":order,
        "cartItems":cartItems,

    }
    return render(request,"user_template/user_view_orders.html",context)
