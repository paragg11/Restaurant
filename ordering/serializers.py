from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['__all__']

    def validate_orderstatus(self, data):
        if ("RECEIVED") in data:
            return data
        elif ("ACCEPTED") in data:
            return data
        elif ("PREPARING") in data:
            return data
        elif ("PREPARED") in data:
            return data
        elif ("INTRANSIT") in data:
            return data
        elif ("DELIVERED") in data:
            return data
        elif ("CANCELED") in data:
            return data  
        else:
            return serializers.ValidationError("Enter RECEIVED or ACCEPTED or PREPARING or PREPARED or INTRANSIT or DELIVERED or CANCELED")
