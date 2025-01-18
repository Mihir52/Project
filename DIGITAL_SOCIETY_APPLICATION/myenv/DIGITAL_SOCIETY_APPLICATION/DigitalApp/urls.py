"""
URL configuration for DIGITAL_SOCIETY_APPLICATION project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from DigitalApp.views import *


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('forgotpassword/', ForgotpasswordView.as_view(), name='forgotpassword'),
    path('verifyotp/', VerifyotpView.as_view(), name='verifyotp'),
    path('resetpassword/', ResetpasswordView.as_view(), name='resetpassword'),
    path('login/', LoginView.as_view(), name='login'),
    path('index/', IndexView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('s_members/', S_membersView.as_view(), name='s_members'),
    path('s_watchmen/', S_watchmenView.as_view(), name='s_watchmen'),
    path('updatemember/ <int:pk>', UpdatememberView.as_view(), name='updatemember'),
    path('deletemember/ <int:pk>', DeletememberView.as_view(), name='deletemember'),
    path('notice/', NoticeView.as_view(), name='notice'),
    path('createnotice/', CreatenoticeView.as_view(), name='createnotice'),
    path('updatenotice/ <int:pk>', UpdatenoticeView.as_view(), name='updatenotice'),
    path('deletenotice/ <int:pk>', DeletenoticeView.as_view(), name='deletenotice'),
    path('createevent/', CreateeventView.as_view(), name='createevent'),
    path('event/', EventView.as_view(), name='event'),
    path('updateevent/ <int:pk>', UpdateeventView.as_view(), name='updateevent'),
    path('deleteevent/ <int:pk>', DeleteeventView.as_view(), name='deleteevent'),
    path('changepassword/', ChangepasswordView.as_view(), name='changepassword'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('deleteuseraccount/', DeleteuseraccountView.as_view(), name='deleteuseraccount')
]
