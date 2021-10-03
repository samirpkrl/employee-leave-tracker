
from django.urls import path
from . views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.leaverequest,name='leaverequest'),
    # path('login/',views.loginuser, name='loginuser'),
    path('register/',views.registeruser,name='registeruser'),
    path('login/', auth_views.LoginView.as_view(template_name='leave/loginuser.html', redirect_authenticated_user=True), name='loginuser'),
    path('userlist/',views.userslist,name='userlist'),
    path('logout/', auth_views.LogoutView.as_view(template_name='leave/logout.html'), name='logout'),
    path('leave_create/',LeaveCreateView.as_view(),name='leave_create'),
    path('leavestatus/', views.leavestatus, name='leavestatus'),
    path('monthwise-report/',views.monthwise_report, name='monthwise_report'),
    path('my-report/',views.my_report,name='myreport')
]