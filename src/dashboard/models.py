from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_platform_admin = models.BooleanField(default=False)