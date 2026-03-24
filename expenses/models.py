from django.db import models
from events.models import Event
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Participants(models.Model):
    full_name = models.CharField(max_length=20, verbose_name='Full name')
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE, verbose_name='Event')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='joined at')
    total_paid = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'), verbose_name='Paid amount', validators=[MinValueValidator(0)])
    total_share = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'), verbose_name='Share amount', validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['full_name', 'event'],
                name='unique_user_event_Participants'
            )
        ]

class Expenses(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    event = models.ForeignKey(Event, related_name='expenses', on_delete=models.CASCADE, verbose_name='Event')
    description = models.TextField(blank=True, verbose_name='Description')
    expense_date = models.DateField(verbose_name='Expense date')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'), verbose_name='Total cost', validators=[MinValueValidator(0)])

class SplitPayment(models.Model):
    participant = models.ForeignKey(Participants, related_name='payments', on_delete=models.CASCADE, verbose_name='participant')
    expense = models.ForeignKey(Expenses, related_name='payments',on_delete=models.CASCADE, verbose_name='expense')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='amount',  validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, verbose_name='Description')
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'expense'],
                name='unique_participant_expense'
            )
        ]

class ExpensePayment(models.Model):
    participant = models.ForeignKey(Participants, related_name='payments_made', on_delete=models.CASCADE, verbose_name='participant')
    expense = models.ForeignKey(Expenses, related_name='payments_made', on_delete=models.CASCADE, verbose_name='expense')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='amount', validators=[MinValueValidator(0)])
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'expense'],
                name='unique_participant_expense_for_expense_payment_model'
            )
        ]
