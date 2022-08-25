from django.db import models
from menu.models import RestaurantMenu

# Create your models here.
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        RECIEVED = "RECIEVED"
        ACCEPTED = "ACCEPTED"
        PREPARING = "PREPARING"
        PREPARPED = "PREPARED"
        IN_TRANSIT = "IN_TRANSIT"
        DELIVERED = "DELIVERED"
        CANCELED = "CANCELED"

orderstatus = models.CharField(max_length=15, choices=orderstatus.choices)
timestamp = models.DateTimeField(auto_now_add=True)
