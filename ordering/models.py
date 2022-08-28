from django.db import models
from menu.models import RestaurantMenu

# Create your models here.
class Order(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(default=0, max_digits=10)

