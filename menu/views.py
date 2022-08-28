from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.shortcuts import render
from .serializers import MenuSerializer
from .models import RestaurantMenu

from rest_framework import permissions, generics

from django.core.paginator import Paginator


# Create your views here.


class MenuList(generics.ListCreateAPIView):
    # def get_queryset(self):
    # food_type = self.request.query_params.get('foodtype')
    # if food_type:
    #     queryset = RestaurantMenu.object.filter(foodtype=food_type)

    pagination_class = PageNumberPagination
    page_size = 1

    queryset = RestaurantMenu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (permissions.AllowAny,)


class MenuListDelete(APIView):

    @swagger_auto_schema()
    def get(self, request, pk):
        queryset = RestaurantMenu.objects.get(pk=pk)
        serializer_class = MenuSerializer(queryset)
        return Response({"data": serializer_class.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema()
    def delete(self, request, pk):
        menu = RestaurantMenu.objects.get(pk=pk)
        menu.delete()
        return Response({"message": "Deleted the menu with id " + str(pk)}, status=status.HTTP_204_NO_CONTENT)

# class MenuDelete(generics.DestroyAPIView):
#     queryset = RestaurantMenu.objects.all()
#     serializer_class = MenuSerializer
