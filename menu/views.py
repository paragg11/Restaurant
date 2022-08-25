from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from django.shortcuts import render
from .serializers import MenuSerializer
from .models import RestaurantMenu

from rest_framework import permissions, generics
# Create your views here.

class MenuDetail(generics.GenericAPIView):

    serializer_class=MenuSerializer
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(request_body=MenuSerializer)
    def post(self, request):

        # serializer=MenuSerializer(data=request.data)
        # permission_classes = (permissions.AllowAny, )
        # queryset = Product.objects.filter(active=True)
        # foodtype = serializer.data.get("foodtype")
        # name = serializer.data.get("name")
        # price = serializer.data.get("price")
        # queryset = RestaurantMenu.objects.filter(active=True) 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
            # menu = RestaurantMenu.objects.create()
            # data = menu.save()
        return Response({
            "foodtype" : menu.foodtype,
            "name" : menu.name,
            "price" : menu.price
        }, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        menu=RestaurantMenu.objects.all()
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

# class ProductListAPIView(generics.ListCreateAPIView):
#     serializer_class = MenuSerializer
#     permission_classes = (permissions.AllowAny, )
#     queryset = Product.objects.filter(active=True)

    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filter_fields = ('category',)
    # search_fields = ['title', 'category__title']


# class ProductDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = ProductDetailSerializer
#     permission_classes = (permissions.AllowAny, )
#     queryset = Product.objects.filter(active=True)