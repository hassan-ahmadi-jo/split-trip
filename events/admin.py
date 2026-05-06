from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(models.EventMembership)
class EventMembershipAdmin(admin.ModelAdmin):
    list_display = ['event_title', 'user_first_name', 'user_email']

    def event_title(self, obj):
        return obj.event.title

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_email(self, obj):
        return obj.user.email

@admin.register(models.EventJoinRequest)
class EventMembershipAdmin(admin.ModelAdmin):
    list_display = ['event_title', 'user_first_name', 'user_email']

    def event_title(self, obj):
        return obj.event.title

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_email(self, obj):
        return obj.user.email
