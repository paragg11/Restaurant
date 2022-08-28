from django.urls import path
from .views import MenuList, MenuDelete

app_name = 'menu'

urlpatterns = [
    path('', MenuList.as_view(), name="MenuList"),
    path('<int:pk>', MenuDelete.as_view(), name="MenuDelete")
]
