from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

import uuid

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_verified = models.BooleanField(default=False)
    # is_onboarded = models.BooleanField(default=False)
    # tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # invited_user = models.BooleanField(default=False)
    # invited_otp_used = models.BooleanField(default=False)

    # objects = UsersManager()
    # USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __unicode__(self):
        return self.email

    @property
    def full_name(self):
        """Returns the User's full name."""
        return '%s %s' % (self.first_name, self.last_name)