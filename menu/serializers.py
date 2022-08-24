from rest_framework import serializers

from .models import RestaurantMenu

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantMenu
        fields = ['foodtype', 'name', 'price']

    def validate_foodtype(self, request):
        if ("VEG") in request:
            return request
        elif ("NONVEG") in request:
            return request
        else:
            return serializers.ValidationError("enter veg or nonveg")

