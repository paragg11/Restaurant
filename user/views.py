from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import User, Verification_Code
from .serializers import RegisterSerializer, UserLoginSerializer, OTPSerializer, VerifyAccountSerializer

from user.emails import send_otp_via_email
from datetime import datetime, timedelta
import logging

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
            msg = {'Message': 'User registered successfully.'}
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user and user.is_verified:
            if not user.invited_otp_used:
                login(request, user)

                user_profile_data = UserProfile.objects.filter(user__email=email).values()
                # Getting token for user
                token = get_tokens_for_user(user)
                if user.invited_user:
                    user.invited_otp_used = True
                    user.save()

                if user.is_onboarded:
                    user_data = {
                        'token': token,
                        'email': user.email,
                        'name': user.full_name,
                        'designation': user_profile_data[0]["designation"],
                        'contact_number': user_profile_data[0]["contact_number"],
                        'location': user_profile_data[0]['location'],
                        'one_time_password_used': user.invited_otp_used,
                        'is_onboarded': user.is_onboarded
                    }
                else:
                    user_data = {
                        'token': token,
                        'email': user.email,
                        'name': user.full_name,
                        'one_time_password_used': user.invited_otp_used,
                        'is_onboarded': user.is_onboarded
                    }

                msg = "user logged in successfully"
                data = {'data': user_data, 'Message': msg}

                return Response(data, status=status.HTTP_200_OK)
            else:
                msg = {'message': "one time password used"}
                return Response(msg, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'not authorized'}, status=status.HTTP_404_NOT_FOUND)


class SendOTP(APIView):

    @swagger_auto_schema(request_body=OTPSerializer)
    def post(self, request):
        try:
            data = request.data
            serializer = OTPSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = User.objects.get(pk=request.data['user'])
                user_email = user.email
                otp = send_otp_via_email(user_email)
                serializer.validated_data['otp'] = otp
                serializer.validated_data['expiry'] = (datetime.now() + timedelta(minutes=15)).time()
                serializer.save()
                return Response({'message': 'verification code sent successfully',
                                 }, status=status.HTTP_200_OK)

            # return Response({'message': 'something went wrong',
            #                  'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error("error occurred while sending otp", exc_info=True)
            raise e


class VerifyOTP(APIView):

    @swagger_auto_schema(request_body=VerifyAccountSerializer)
    def post(self, request):
        try:
            data = request.data
            user_id = data['user']
            user = User.objects.filter(pk=user_id)
            if user:
                user = User.objects.get(pk=user_id)
                serializer = VerifyAccountSerializer(data=data)
            else:
                return Response({
                    'status': 400,
                    'message': "Invalid user id please register with our system."
                }, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                # user = User.objects.get(pk=request.data['user'])
                # user_email = user.email
                pk = serializer.data['user']
                otp = serializer.data['otp']
                otp_obj = Verification_Code.objects.filter(user_id=pk, otp=otp)
                if otp_obj:
                    otp_obj = otp_obj.values()[0]
                else:
                    return Response({
                        'status': 400,
                        'message': "Wrong otp"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if otp_obj['otp'] != otp:
                    return Response({
                        'status': 400,
                        'message': "incorrect otp"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if datetime.datetime.now().time() > otp_obj['expiry']:
                    return Response({
                        'status': 400,
                        'message': "otp expired"
                    }, status=status.HTTP_400_BAD_REQUEST)

                user.is_verified = True
                user.save()
                return Response({
                    'status': 200,
                    'message': 'account verified successfully'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error("error occurred while verifying otp", exc_info=True)
            raise e
