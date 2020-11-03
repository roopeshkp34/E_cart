from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from e_cart_app.models import Dealer,CustomUser,Product




def user__home(request):
    products=Product.objects.all()
    print(products)
    context= {
        "products":products,
    }
    return render(request,"user_template/user_home.html",context)