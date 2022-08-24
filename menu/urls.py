from django.urls import path
from .views import MenuDetail
app_name= 'menu'

urlpatterns = [
    path('', MenuDetail.as_view(), name="Menu"),
]