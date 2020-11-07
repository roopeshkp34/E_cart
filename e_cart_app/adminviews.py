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
    return render(request,'admin_template/admin_home.html')




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
def manage_users(request):
    return render(request,"admin_template/manage_user_template.html")




 

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
    