from django.db import models

# Create your models here.

class SiteSettings(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='Is active')
    conract_email = models.EmailField(blank=True, verbose_name='Email address')
    github_url = models.URLField(blank=True, max_length=200, verbose_name='GitHub url')
    linkedin_url =models.URLField(blank=True, max_length=200, verbose_name='Linkedin url')
    website_url = models.URLField(blank=True, max_length=200, verbose_name='Website url')

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

class ContactSender(models.Model):
    email = models.EmailField(verbose_name='Email address')
    is_sender_member = models.BooleanField(default=False, verbose_name='Is user member in website')

    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        verbose_name = 'Contact sender'
        verbose_name_plural = 'Contact senders'

class ContactMessage(models.Model):
    sender = models.ForeignKey(ContactSender, related_name='messages', on_delete=models.CASCADE, verbose_name='Message sender')
    message = models.TextField(max_length=2000, verbose_name='Message')
    sent_at = models.DateTimeField(auto_now_add=True ,verbose_name='Sent at')
    is_replied = models.BooleanField(default=False, verbose_name='Is replied')

    class Meta:
        verbose_name = 'Contact message'
        verbose_name_plural = 'Contact messages'
