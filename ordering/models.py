from django.db import models
from menu.models import RestaurantMenu
from user.models import User

# Create your models here.


class Order(models.Model):

    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    menu_id = models.ForeignKey(RestaurantMenu, on_delete=models.CASCADE, related_name="ordering")
    quantity = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    is_active = models.BooleanField(default=True)


