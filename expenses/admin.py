from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'event__title', 'total_paid', 'total_share']
    list_filter = ['full_name', 'event__title']

    
@admin.register(models.Expenses)
class moduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'event__title', 'total_amount']
    list_filter = ['event__title']


@admin.register(models.ParticipantExpense)
class ParticipantExpenseAdmin(admin.ModelAdmin):
    list_display = ['participant__full_name', 'expense__title', 'paid_amount', 'share_amount']
    list_filter = ['participant__full_name', 'expense__title']
