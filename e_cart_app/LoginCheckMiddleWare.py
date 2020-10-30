from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "e_cart_app.adminviews":
                    pass
                elif modulename == "e_cart_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")

            elif user.user_type == "2":
                if modulename == "e_cart_app.dealerviews":
                    pass
                elif modulename == "e_cart_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("dealer_home")

            # elif user.user_type == "3":
            #     if modulename == "e_cart_app.customerviews":
            #         pass
            #     elif modulename == "e_cart_app.views" or modulename == "django.views.static":
            #         pass
            #     else:
            #         return redirect("employee_home")
            else:
                return redirect("dealer_login")



                
        else:
            if request.path == reverse("admin_login") or request.path == reverse("admin_dologin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return redirect("admin_login")

            
