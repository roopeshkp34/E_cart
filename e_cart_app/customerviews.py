from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from e_cart_app.models import Dealer,CustomUser,Product,Order,OrderItem
import json


def user__home(request):
    if request.user.is_authenticated:
        admin=request.user.id
        order, created = Order.objects.get_or_create(customer=admin,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    products=Product.objects.all()
    context= {
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
        order ={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    context ={
        "product":product,
        "cartItems":cartItems,
    }
    return render(request,"user_template/user_view_product.html",context)



def user_cart(request):
    if request.user.is_authenticated:
        admin=request.user.id
        order, created = Order.objects.get_or_create(customer=admin,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}
        cartItems=order['get_cart_items']
    context ={
        "items":items,
        "order":order,
        "cartItems":cartItems,
    }
    return render(request,"user_template/user_cart.html",context)



def user_checkout(request):
    if request.user.is_authenticated:
        admin=request.user.id
        order, created = Order.objects.get_or_create(customer=admin,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items

    else:
        items=[]
        order ={'get_cart_total':0,'get_cart_items':0}
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

    customer=request.user.id
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