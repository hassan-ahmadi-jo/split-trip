from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'is_email_active', 'email_active_code']
    list_filter = ['is_email_active']
    list_editable = ['is_email_active']
    list_per_page = 20

@admin.register(models.EmailActivation)
class EmailActivationAdmin(admin.ModelAdmin):
    list_display = ['user__first_name', 'user__email', 'expires_at']
    list_editable = ['expires_at']
    list_per_page = 20