from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from e_cart_app.models import Dealer,CustomUser,Product,Order,OrderItem




def user__home(request):
    products=Product.objects.all()
    context= {
        "products":products,
    }
    return render(request,"user_template/user_home.html",context)


def user_view_product(request,product_id):
    product=Product.objects.get(id=product_id)
    context ={
        "product":product,
    }
    return render(request,"user_template/user_view_product.html",context)



def user_cart(request):
    items = OrderItem.objects.all()
    order = Order.objects.all()
    print(order.count())
    context ={
        "items":items,
        "order":order,
    }
    return render(request,"user_template/user_cart.html",context)



def user_checkout(request):
    items = OrderItem.objects.all()
    context ={
            "items":items,
        }
    return render(request,"user_template/check_out.html",context)

