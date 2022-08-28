from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import RestaurantMenu


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantMenu
        fields = ['foodtype', 'name', 'price', 'id']

    def validate_foodtype(self, request):
        if ("VEG") in request:
            return request
        elif ("NONVEG") in request:
            return request
        else:
            return serializers.ValidationError("enter veg or nonveg")

    def validate_price(self, data):
        if data < 1:
            raise ValidationError('This number is lesser than 1')
        return data