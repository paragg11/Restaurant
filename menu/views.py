from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.shortcuts import render
from .serializers import MenuSerializer
from .models import RestaurantMenu

# Create your views here.

class MenuDetail(APIView):

    @swagger_auto_schema(request_body=MenuSerializer)
    def post(self, request):
        serializer=MenuSerializer(data=request.data)
        if serializer.is_valid():
            foodtype = serializer.data.get("foodtype")
            name = serializer.data.get("name")
            price = serializer.data.get("price")
            menu = RestaurantMenu.objects.create()
            data = menu.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        menu=RestaurantMenu.objects.all()
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

