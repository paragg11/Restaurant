from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User, Verification_Code, UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'designation', 'location', 'contact_number')

    def create(self, validated_data, *args, **kwargs):

        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

    def update(self, instance, validated_data, *args, **kwargs):
        nested_serializer = self.fields['user']
        nested_instance = instance.user
        nested_data = validated_data.pop('user')
        nested_serializer.update(nested_instance, nested_data)
        return super(UserProfileSerializer, self).update(instance, validated_data)

    def validate(self, data):

        if data.get('contact_number') == "":
            raise serializers.ValidationError("Contact number should not be empty.")
        if data.get('designation') == "":
            raise serializers.ValidationError("Designation should not be empty.")
        if data.get('location') == "":
            raise serializers.ValidationError("Location should not be empty.")
        if not self.partial:
            if data.get('contact_number') is None:
                raise serializers.ValidationError("Contact number is required.")
            if data.get('designation') is None:
                raise serializers.ValidationError("Designation is required.")
            if data.get('location') is None:
                raise serializers.ValidationError("Location is required.")

        return data
