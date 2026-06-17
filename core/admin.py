from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['conract_email', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']

@admin.register(models.ContactSender)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_sender_member']
    list_filter = ['is_sender_member']

@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender__email', 'sender__is_sender_member', 'sent_at', 'is_replied']
    list_editable = ['is_replied']
    list_filter = ['sender__is_sender_member', 'is_replied']
