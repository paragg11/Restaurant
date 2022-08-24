from django.db import models

# Create your models here.
class RestaurantMenu(models.Model):
    class FoodType(models.TextChoices):
        VEG = "VEG"
        NONVEG = "NONVEG"

    foodtype = models.CharField(max_length=10, choices=FoodType.choices)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)


