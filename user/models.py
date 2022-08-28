from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import UserManager
from phonenumber_field.modelfields import PhoneNumberField

import uuid

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_number = PhoneNumberField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)
    # tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True)
    # updated_at = models.DateTimeField(auto_now=True)
    invited_user = models.BooleanField(default=False)
    invited_otp_used = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __unicode__(self):
        return self.email

    @property
    def full_name(self):
        """Returns the User's full name."""
        return '%s %s' % (self.first_name, self.last_name)


class VerificationCode(models.Model):
    class Event(models.TextChoices):
        SIGN_UP = 'Sign_Up'
        FORGOT_PASSWORD = 'Forgot_Password'

    event = models.CharField(max_length=30, choices=Event.choices)
    user = models.ForeignKey(User, related_name="User_verification", on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)
    expiry = models.TimeField(auto_now=False, null=True, blank=True)


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, related_name="User", on_delete=models.CASCADE, primary_key=True)
#     location = models.CharField(max_length=100, blank=True, null=True)
#     contact_number = PhoneNumberField(blank=True, null=True)
#
#     # profile_picture = models.ImageField()
#
#     class Meta:
#         verbose_name = 'User Profile'
#         verbose_name_plural = 'User Profiles'


