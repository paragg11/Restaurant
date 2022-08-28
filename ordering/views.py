from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

from .serializers import OrderSerializer
from .models import Order

from user.models import User
from menu.models import RestaurantMenu

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import decimal

import logging


# Create your views here.


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):

        try:
            user = User.objects.get(pk=request.data["user_id"])
            if user:
                menu = RestaurantMenu.objects.get(id=request.data["menu_id"])
                if menu:
                    order = Order(menu_id=menu,
                                  user_id=user,
                                  quantity=decimal.Decimal(str(request.data["quantity"]) + ".00"))
                    order.save()
                    return Response({'message': 'Order sent successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'menu id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'user id does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error("error occurred while verifying user", exc_info=True)
            raise e


class UserOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            queryset = Order.objects.filter(user_id=user_id)
            allmenu = list(queryset)
            sum = 0
            for data in allmenu:
                print(data.menu_id.price)
                sum = sum + data.menu_id.price * data.quantity
                serializer_class = OrderSerializer(queryset, many=True)
                return Response({"data": serializer_class.data, "total": sum}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"user_id": "id does not exist"})
