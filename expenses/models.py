from django.db import models
from events.models import Event

# Create your models here.

class Participants(models.Model):
    full_name = models.CharField(max_length=20, verbose_name='Full name')
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE, verbose_name='Event')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='joined at')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['full_name', 'event'],
                name='unique_user_event_Participants'
            )
        ]

# class Expenses(models.Model):
#     title = models.CharField(max_length=50, verbose_name='Title')
#     event = models.ForeignKey(Event, related_name='expenses', on_delete=models.CASCADE, verbose_name='Event')
#     description = models.TextField(blank=True, verbose_name='Description')
#     expense_date = models.DateField(verbose_name='Expense date')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
#     updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')