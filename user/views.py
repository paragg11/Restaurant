from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

from serializer import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from models import User

# Create your views here.


class RegisterUserView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = User.objects.create(email=email)
            user.set_password(request.data.get('password'))
            user.is_active = False
            user.save()
            msg = {'Message': 'User registered successfully. Please verify email to continue.'}
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
