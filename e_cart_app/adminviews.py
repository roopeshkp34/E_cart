from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect


def admin_login(request):
    return render(request,'admin_template/admin_login.html')

def admin_home(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                # return HttpResponse("hi")
                return redirect("home")
            else:
                messages.error(request,'Invalid Login Details')
                return HttpResponseRedirect("admin_login")
        except:
            messages.error(request,'Invalid Login Details')
            return HttpResponseRedirect("admin_login")

    else:
        return render(request,'admin_template/admin_login.html')

def home(request):
    return render(request,'admin_template/admin_home.html')
    