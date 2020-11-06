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
from e_cart_app import adminviews,dealerviews,customerviews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    
    #Admin views

    path('admin/', admin.site.urls),
    path('admin_login',adminviews.admin_login,name='admin_login'),
    path('admin_dologin',adminviews.admin_dologin,name='admin_dologin'),
    path('admin_home',adminviews.admin_home,name='admin_home'),
    path('admin_logout',adminviews.admin_logout,name='admin_logout'),
    path('manage_dealer',adminviews.manage_dealer,name='manage_dealer'),
    path('manage_users',adminviews.manage_users,name='manage_users'),
    path('add_dealer',adminviews.add_dealer,name='add_dealer'),
    path('save_add_dealer',adminviews.save_add_dealer,name='save_add_dealer'),
    path('edit_dealer/<str:dealer_id>',adminviews.edit_dealer,name='edit_dealer'),
    path('save_edit_dealer',adminviews.save_edit_dealer,name='save_edit_dealer'),
    path('delete_dealer/<str:dealer_id>',adminviews.delete_dealer,name='delete_dealer'),
    path('admin_view_product',adminviews.admin_view_product,name='admin_view_product'),










    #Dealer Views
    path('dealer_login',dealerviews.dealer_login,name='dealer_login'),
    path('dealer_dologin',dealerviews.dealer_dologin,name='dealer_dologin'),
    path('dealer_home',dealerviews.dealer_home,name='dealer_home'),
    path('dealer_logout',dealerviews.dealer_logout,name='dealer_logout'),
    path('manage_product',dealerviews.manage_product,name='manage_product'),
    path('add_product',dealerviews.add_product,name='add_product'),
    path('add_product_save',dealerviews.add_product_save,name='add_product_save'),
    path('edit_product/<str:product_id>',dealerviews.edit_product,name='edit_product'),
    path('save_edit_product',dealerviews.save_edit_product,name='save_edit_product'),
    path('delete_product/<str:product_id>',dealerviews.delete_product,name='delete_product'),









    #user Views
    path("",customerviews.user__home,name="user_home"),
    path("user_view_product/<str:product_id>",customerviews.user_view_product,name="user_view_product"),
    path("user_cart",customerviews.user_cart,name="user_cart"),
    path("user_checkout",customerviews.user_checkout,name="user_checkout"),
    path("update_item/",customerviews.updateItem,name="update_item"),





]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
