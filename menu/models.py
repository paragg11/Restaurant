from django.db import models

# Create your models here.
class RestaurantMenu(models.Model):
    class FoodType(models.TextChoices):
        VEG = "VEG"
        NONVEG = "NONVEG"

    foodtype = models.CharField(max_length=10, choices=FoodType.choices)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)


