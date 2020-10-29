"""e_cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from e_cart_app import adminviews

urlpatterns = [
    
    
    #Admin views

    path('admin/', admin.site.urls),
    path('admin_login',adminviews.admin_login,name='admin_login'),
    path('admin_dologin',adminviews.admin_dologin,name='admin_dologin'),
    path('admin_home',adminviews.admin_home,name='admin_home'),
    path('admin_home',adminviews.admin_home,name='admin_home'),
    path('manage_dealer',adminviews.manage_dealer,name='manage_dealer'),
    path('manage_users',adminviews.manage_users,name='manage_users'),
    path('add_dealer',adminviews.add_dealer,name='add_dealer'),
    path('save_add_dealer',adminviews.save_add_dealer,name='save_add_dealer'),






    #Dealer Views


    #user Views


]
