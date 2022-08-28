from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import User, VerificationCode
from .serializers import RegisterSerializer, UserLoginSerializer, OTPSerializer, VerifyAccountSerializer, \
    UserProfileSerializer, UserSerializer

from user.emails import send_otp_via_email
from datetime import timedelta, datetime
import logging

from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['email'] = user.email
    # if user.tenant:
    #     refresh['tenant_id'] = str(user.tenant.id)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
            user.is_active = True
            user.is_superuser = True
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
        print(email, type(email))
        print(password, type(password))

        # db_user = User.objects.filter(email=email)
        # print(db_user)
        # check_pwd_bool = db_user.check_password(password)
        # print(check_pwd_bool)

        # user_1 = authenticate(username=email, password=password)
        # print(user_1)

        user = authenticate(email=email, password=password)
        print(user)

        if user and user.is_verified:
            if not user.invited_otp_used:
                login(request, user)

                user_profile_data = User.objects.filter(email=email).values()
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
                                 # 'otp': user.emails
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
            # print(user_id)
            user = User.objects.filter(pk=user_id)
            # print(user)
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
                otp_obj = VerificationCode.objects.filter(user_id=pk, otp=otp)
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
                if datetime.now().time() > otp_obj['expiry']:
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


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    # def get(self, request, *args, **kwargs):
    #
    #     user_profile = UserProfile.objects.get(user=request.user)
    #     serializer = UserProfileSerializer(user_profile)
    #     if User.is_verified:
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):


        try:
            profile = User.objects.get(pk=pk)
            # serializer = UserSerializer(instance=profile, data=profile)
            # if serializer.is_valid():
            #     return Response({'data': serializer.data, 'message': 'user profile updated successfully.'},
            #                     status=status.HTTP_200_OK)
            # else:
            #     return Response({"user_id": "id does not exist"})

            profile_dic = {"id": profile.id, "email": profile.email, "first name": profile.first_name,
                           "last name": profile.last_name, "location": profile.location,
                           "contact number": str(profile.contact_number)
                           }
            return Response({'data': profile_dic, 'message': 'user id found successfully.'},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"user_id": "id does not exist"})

    # @swagger_auto_schema(request_body=UserProfileSerializer)
    # def post(self, request, *args, **kwargs):
    #
    #     user_profile = UserProfile(user=request.user)
    #     serializer = UserProfileSerializer(user_profile, data=request.data)
    #     if serializer.is_valid():
    #         if User.objects.get(id=request.user.id).is_verified:
    #             # check if user is onboarded
    #             if not User.objects.get(id=request.user.id).is_onboarded:
    #                 serializer.save()
    #                 user_onboarded = User.objects.get(id=request.user.id)
    #                 user_onboarded.is_onboarded = True
    #                 user_onboarded.save()
    #                 return Response({'data': serializer.data, 'message': 'user profile added successfully.'},
    #                                 status=status.HTTP_201_CREATED)
    #             else:
    #                 return Response({'message': 'user has already onboarded'}, status=status.HTTP_409_CONFLICT)
    #         else:
    #             return Response({'message': 'user is not verified'}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def put(self, request, pk, *args, **kwargs):

        user_profile = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(instance=user_profile, data=request.data)

        if serializer.is_valid():
            if User.objects.get(id=request.user.id).is_verified:
                serializer.save()
                return Response({'data': serializer.data, 'message': 'user profile updated successfully.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'user is not verified'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def patch(self, request, pk, *args, **kwargs):

        user_profile = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(instance=user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            if User.objects.get(id=request.user.id).is_verified:
                serializer.save()
                return Response({'data': serializer.data, 'message': 'user profile updated successfully.'},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
