from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User, Verification_Code


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirmPassword')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError(
                {"password": "password fields didn't match."})
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6, required=False, read_only=True)
    expiry = serializers.TimeField(required=False, read_only=True)

    class Meta:
        model = Verification_Code
        fields = ['user', 'event', 'otp', 'expiry']


class VerifyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification_Code
        fields = ['user', 'otp']

    def validated(self, data):
        User

