from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import *
from datetime import date
import datetime
from django.db.models import Sum
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
decor = [login_required(login_url='loginuser')]
# Create your views here.

@login_required(login_url='loginuser')
def leaverequest(request):
    return render(request,'base.html')

@login_required(login_url='loginuser')
@allowed_users
def userslist(request):
    template='leave/userlist.html'
    objects=User.objects.all()
    context={
        'objects': objects,
    }
    return render(request,template,context)

@login_required(login_url='loginuser')
@allowed_users
def registeruser(request):
    template = "leave/register.html"
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Email already exists! Please enter a different email.')
                return redirect('registeruser')
            else:  
                obj=form.save(commit=False)
                obj.is_staff=True
                obj.save()
                return redirect('login')
        
    else:
        form = UserRegisterForm()
    context={
        'form':form,
    }
    return render(request, template, context)

@method_decorator(decor, name='dispatch')
class LeaveCreateView(CreateView):
    template_name = 'leave/leave_request.html'
    
    form_class = LeaveForm
    success_url = 'leaverequest'

    def form_valid(self, form): 
        obj=form.save(commit=False)
        obj.userid=self.request.user
        obj.save()
        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form):  
        return  render(self.request,'leave/leave_request.html',{'form':form,'errors': form.errors,})
        
    def get_success_url(self):
        return reverse("leaverequest")

@login_required(login_url='loginuser')
@allowed_users
def leavestatus(request):
    template='leave/leavestatus.html'

    leave_objects=Empleave.objects.all()
    if 'userid' in request.GET:
        usr=request.GET['userid']
        leave_objects= leave_objects.filter(userid=usr)
    
    usrobj=User.objects.all()
    tot=leave_objects.aggregate(Sum('days')).get('days__sum',0) or 0
    context={
        'objects': leave_objects,
        'usrobj':usrobj,
        'total':tot
    }
    return render(request,template,context)

@login_required(login_url='loginuser')
def my_report(request):
    leave_obj=Empleave.objects.filter(userid=request.user)
    tot=leave_obj.aggregate(Sum('days')).get('days__sum',0) or 0
    context={
        'obj':leave_obj,
        'total':tot
    }
    return render(request,'leave\my_leave_report.html',context)

@login_required(login_url='loginuser')
@allowed_users
def monthwise_report(request):
    template='leave\monthwise_report.html'

    all_leave={}
    uid=None
    usrobj=User.objects.all()
    obj= Empleave.objects.all()
    if 'userid' in request.GET:
        usr=request.GET['userid']
        uid=usrobj.get(id=usr) or None
        obj= obj.filter(userid=usr)
    months = obj.dates("from_date", kind="month")
    for i in months:
        month_invs = obj.filter(from_date__month=i.month)
        month_total = month_invs.aggregate(Sum("days")).get("days__sum",0) or 0
        #print(f"Month: {i}, Total: {month_total}")
        #print(i.strftime("%B"),month_total)
        all_leave[i]=i.strftime("%B"),month_total
    context={
        'obj':obj,
        'usrobj':usrobj,
        'leave':all_leave,
        'uid':uid
    }
    return render(request,template,context)
