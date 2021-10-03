from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(view_func):
    def allowed_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not autorized to view this page. Please contact your administrator')
    
    return allowed_func
   