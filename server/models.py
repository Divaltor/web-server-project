from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.validators import MaxLengthValidator
from django.db import models

class UserManager(BaseUserManager):

    def _create_user(self, email: str, password: str | None, **extra_fields: t.Any) -> User:
        """Create and save a user with the given email, and password."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields) -> User:
        """Create user."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> User:
        """Create superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:  # pragma: no cover
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:  # pragma: no cover
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Item(BaseModel):
    sku = models.TextField(unique=True)
    name = models.TextField()
    description = models.TextField(blank=True)
    buy_price = models.DecimalField(decimal_places=2, max_digits=10)
    sell_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='items')

    def __str__(self):
        return self.name
