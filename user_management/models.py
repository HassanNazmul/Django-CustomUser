from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.db import models


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=60)

    # Role differentiation
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Permission-related fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    # Set verbose_name for your model
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users List"

    def clean(self):
        # Validate the conditions before saving
        if self.is_student and (self.is_admin or self.is_staff):
            raise ValidationError("A student cannot be an admin or staff.")

        if self.is_admin and not self.is_staff:
            raise ValidationError("An admin must also be staff.")

    def save(self, *args, **kwargs):
        # Automatically activate the user if any permission field is selected
        if self.is_superuser or self.is_staff or self.is_admin or self.is_student:
            self.is_active = True
        else:
            self.is_active = False

        # Enforce role constraints
        if self.is_student:
            self.is_admin = False
            self.is_staff = False

        if self.is_admin:
            self.is_staff = True
            self.is_student = False

        if self.is_superuser:
            self.is_admin = True
            self.is_staff = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
