from django.urls import path
from .views import MenuList, MenuListDelete

app_name = 'menu'

urlpatterns = [
    path('', MenuList.as_view(), name="MenuList"),
    path('<int:pk>', MenuListDelete.as_view(), name="MenuDetail"),
    # path('<int:pk>', MenuDelete.as_view(), name="MenuDelete")
]
