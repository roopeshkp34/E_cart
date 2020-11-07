from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from e_cart_app.models import Order,OrderItem,Product,ShippingAdress,Customer,CustomUser,Dealer
import json
import datetime
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages





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


def signup(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        mobile_number= request.POST.get('mobile_number')

        user = CustomUser.objects.create_user(username = username, password = password, email = email,first_name=password,last_name=mobile_number,user_type=3)
        # user.customer.mobile_number=mobile_number
        user.save()
        return redirect('/')

    else:
        return render(request,'user_template/user_signup.html')





def user__home(request):
    # if request.user.is_superuser:
    #     admin=request.user.id
    #     order, created = Order.objects.get_or_create(customer=admin,complete=False)
    #     items=order.orderitem_set.all()
    #     cartItems=order.get_cart_items
    if request.user.is_authenticated:
        # login_user = request.user
        # login_name = request.user.username
        # login_email = request.user.email
        # admin, created = Customer.objects.get_or_create(admin = login_user, name = login_name, email = login_email)
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
    context= {
        "items":items,
        "products":products,
        "cartItems":cartItems,
    }
    return render(request,"user_template/user_home.html",context)


def user_view_product(request,product_id):
    product=Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        admin=request.user.id
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

    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']

    context ={
        "items":items,
        "order":order,
        "cartItems":cartItems,

    }
    return render(request,"user_template/check_out.html",context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("Action:", action)
    print("ProductId:", productId)

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    
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

        if order.shipping == 'True':
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],

            )
    else:
        print("user is not loged in")
    return JsonResponse('Payment complete' , safe=False) 
