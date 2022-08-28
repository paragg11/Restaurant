from django.urls import path
from .views import OrderView, UserOrder

app_name = 'ordering'


urlpatterns = [
    path('', OrderView.as_view(), name="Orders"),
    path('<int:user_id>', UserOrder.as_view(), name='user_order'),
]

