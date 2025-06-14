from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    username = models.CharField(unique=True)
    password = models.CharField()
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return self.username