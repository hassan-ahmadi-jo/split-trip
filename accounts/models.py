from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email address')
    is_email_active = models.BooleanField(default=False, verbose_name='Is email active')
    email_active_code = models.CharField(max_length=6, verbose_name='Email active code')

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save(*args, **kwargs)
    

class EmailActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_activation', verbose_name='User')
    expires_at = models.DateTimeField(default= timezone.now ,verbose_name='Expiration Time')
