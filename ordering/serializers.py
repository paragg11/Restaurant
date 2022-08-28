from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "timestamp", "menu_id", "quantity", "user_id", "is_active"]

    def validate_quantity(self, value):
        if value >= 0:
            return value
        else:
            raise serializers.ValidationError("Please input valid balance")


