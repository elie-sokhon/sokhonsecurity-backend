from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)  # ✅ New full name field
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)  # ✅ Ensure email is unique
    is_verified = models.BooleanField(default=False)
 
