from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.conf import settings

# Create your models here.

def generate_email_active_code():
    if settings.USE_FIXED_EMAIL_ACTIVATION_CODE:
        return settings.FIXED_EMAIL_ACTIVATION_CODE
    return str(random.randint(100000, 999999))

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email address')
    is_email_active = models.BooleanField(default=False, verbose_name='Is email active')
    email_active_code = models.CharField(max_length=6, verbose_name='Email active code')

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)
    

# class ResetPassword