from django.urls import path

from .views import RegisterUserView, UserLoginView, SendOTP, VerifyOTP, UserProfileView

app_name = 'base'

urlpatterns = [

    path('signup', RegisterUserView.as_view(), name='SignUp'),
    path('login', UserLoginView.as_view(), name='login-user'),
    path('generate-otp', SendOTP.as_view(), name='generate-otp'),
    path('verify-otp', VerifyOTP.as_view(), name='verify-otp'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user-profile-detail'),
    # path('profile/<int:pk>', UserProfileView.get(pk=pk).as_view(), name='user-profile-detail')

    

]