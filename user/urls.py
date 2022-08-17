from django.urls import path

from views import RegisterUserView

app_name = 'base'

urlpatterns = [

    path('signup', RegisterUserView.as_view(), name='SignUp')

]