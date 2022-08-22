from django.urls import path

from .views import RegisterUserView, UserLoginView, SendOTP, VerifyOTP

app_name = 'base'

urlpatterns = [

    path('signup', RegisterUserView.as_view(), name='SignUp'),
    path('login', UserLoginView.as_view(), name='login-user'),
    path('generate-otp', SendOTP.as_view(), name='generate-otp'),
    path('verify-otp', VerifyOTP.as_view(), name='verify-otp'),


]