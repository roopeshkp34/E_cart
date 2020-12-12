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
from django.urls import path,include
from e_cart_app import adminviews,dealerviews,customerviews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    
    #Admin views
    path('accounts/', include('allauth.urls')),


    path('admin/', admin.site.urls),
    path('admin_login',adminviews.admin_login,name='admin_login'),
    path('admin_dologin',adminviews.admin_dologin,name='admin_dologin'),
    path('admin_home',adminviews.admin_home,name='admin_home'),
    path('admin_logout',adminviews.admin_logout,name='admin_logout'),
    path('manage_dealer',adminviews.manage_dealer,name='manage_dealer'),
    path('view_dealer/<str:dealer_id>',adminviews.view_dealer,name='view_dealer'),
    path('admin_edit_product/<str:product_id>',adminviews.admin_edit_product,name='admin_edit_product'),
    path('save_admin_edit_product',adminviews.save_admin_edit_product,name='save_admin_edit_product'),
    path('manage_users',adminviews.manage_users,name='manage_users'),
    path('add_dealer',adminviews.add_dealer,name='add_dealer'),
    path('save_add_dealer',adminviews.save_add_dealer,name='save_add_dealer'),
    path('edit_dealer/<str:dealer_id>',adminviews.edit_dealer,name='edit_dealer'),
    path('save_edit_dealer',adminviews.save_edit_dealer,name='save_edit_dealer'),
    path('delete_dealer/<str:dealer_id>',adminviews.delete_dealer,name='delete_dealer'),
    path('admin_view_product',adminviews.admin_view_product,name='admin_view_product'),
    path('admin_delete_product/<str:product_id>',adminviews.admin_delete_product,name="admin_delete_product"),
    path('admin_deactive/<str:product_id>',adminviews.admin_deactive,name="admin_deactive"),
    path('admin_active/<str:product_id>',adminviews.admin_active,name="admin_active"),
    path('admin_order_view',adminviews.admin_order_view,name='admin_order_view'),
    path('add_category',adminviews.add_category,name="add_category"),
    path('manage_category',adminviews.manage_category,name="manage_category"),
    path('block_user/<str:user_id>',adminviews.block_user,name="block_user"),
    path('unblock_user/<str:user_id>',adminviews.unblock_user,name="unblock_user"),















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
    path('dealer_order_view',dealerviews.dealer_order_view,name='dealer_order_view'),
    path('update_order/',dealerviews.update_order,name='update_order'),
    path('add_offers',dealerviews.add_offers,name='add_offers'),
    path('manage_offers',dealerviews.manage_offers,name='manage_offers'),
    path('add_category_offers',dealerviews.add_category_offers,name='add_category_offers'),
    path('add_category_offers_save',dealerviews.add_category_offers_save,name='add_category_offers_save'),
    path('manage_reports',dealerviews.manage_reports,name='manage_reports'),
    path('sales_report',dealerviews.sales_report,name='sales_report'),















    #user Views
    path('mobile',customerviews.mobile,name='mobile'),
    path('otp',customerviews.otp,name='otp'),

    path("",customerviews.user__home,name="user_home"),
    path("user_login",customerviews.user_login,name="user_login"),
    path("user_logout",customerviews.user_logout,name="user_logout"),
    path("signup",customerviews.signup,name="signup"),
    path("reffral_signup/<str:reff_code>",customerviews.reffral_signup,name="reffral_signup"),

    path("user_view_product/<str:product_id>",customerviews.user_view_product,name="user_view_product"),
    path("user_cart",customerviews.user_cart,name="user_cart"),
    path("user_checkout/",customerviews.user_checkout,name="user_checkout"),
    path("update_item/",customerviews.updateItem,name="update_item"),
    path("process_order/",customerviews.processOrder,name="process_order"),
    path("user_view_orders",customerviews.user_view_orders,name="user_view_orders"),
    path('getshipping/',customerviews.Getshipping.as_view()),
    path('user_view_profile',customerviews.user_view_profile,name="user_view_profile"),
    path('check_username_exist',customerviews.check_username_exist,name="check_username_exist"),
    path('check_email_exist',customerviews.check_email_exist,name="check_email_exist"),
    path('check_mobile_exist',customerviews.check_mobile_exist,name="check_mobile_exist"),









]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
