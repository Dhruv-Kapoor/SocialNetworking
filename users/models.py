from typing import Any
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    @classmethod
    def normalize_email(cls, email):
        return super().normalize_email(email.lower())
    
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs) -> Any:
        return super().create_superuser('', *args, **kwargs)

    def create_user(self, *args, **kwargs) -> Any:
        return super().create_user('', *args, **kwargs)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self) -> str:
        return self.full_name or self.email

    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]
