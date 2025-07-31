from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username