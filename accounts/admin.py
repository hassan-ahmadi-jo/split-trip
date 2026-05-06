from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'is_email_active', 'email_active_code']
    list_filter = ['is_email_active']
    list_editable = ['is_email_active']
    list_per_page = 20