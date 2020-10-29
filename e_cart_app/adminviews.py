from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from e_cart_app.models import Dealer,CustomUser


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
                return redirect("admin_home")
            else:
                messages.error(request,'Invalid Login Details')
                return HttpResponseRedirect("admin_login")
        except:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("admin_login")

    else:
        return render(request,'admin_template/admin_login.html')


def admin_home(request):
    return render(request,'admin_template/admin_home.html')



def add_dealer(request):
    return render(request,'admin_template/add_dealer.html')


def save_add_dealer(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        address=request.POST.get('address')
        mobile_number=request.POST.get('mobile')

        user=CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name,user_type=2)
        # dealer=Dealer.objects.get(id=user)
        user.dealer.address=address
        user.dealer.mobile_number=mobile_number
        user.save()
        return redirect("/add_dealer")
    else:
        return redirect("/add_dealer")


    


def manage_dealer(request):
    dealers=Dealer.objects.all()
    context={
        "dealers":dealers,
    }
    return render(request,"admin_template/manage_dealer_template.html",context)


def manage_users(request):
    return render(request,"admin_template/manage_user_template.html")

    