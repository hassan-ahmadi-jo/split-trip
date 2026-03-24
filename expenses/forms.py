from django import forms
from . import models

class ParticipantsForm(forms.ModelForm):
    def __init__(self, *args, event = None, update_object = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        self.update_object = update_object
    class Meta:
        model = models.Participants
        fields = ['full_name']
        labels = {
            'full_name': 'Full name'
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a participant name'
            })
        }

    def clean_full_name(self):
        data = self.cleaned_data["full_name"]
        event = self.event
        if len(data) < 3:
            raise forms.ValidationError('The name must be at least 3 characters.')
        elif len(data) > 20:
            raise forms.ValidationError('The name must be no more than 20 characters.')
        elif event and event.participants.filter(full_name__iexact=data).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This participant already exists.')
        return data
    
    def save(self, commit = True):
        instance = super().save(False)
        if self.event is not None and self.update_object is False:
            instance.event = self.event
        if commit:
            instance.save()
        return instance

class ExpensesForm(forms.ModelForm):
    def __init__(self, *args, event = None, update_object = False, **kwargs):
        self.event = event
        self.update_object = update_object
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Expenses
        fields = ['title', 'expense_date', 'description']
        labels = {
            'title': 'What was this expense for?',
            'description': 'Additional Notes',
            'expense_date': 'When did you pay?',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'wizard-input',
                'placeholder': 'e.g., Dinner at Milad Tower, Taxi to airport...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'wizard-input',
                'placeholder': 'Any extra details about this expense? (Optional)',
                'rows':'3'
            }),
            'expense_date': forms.DateInput(attrs={
                'class': 'wizard-input',
                'type': 'date', 
            }),
        }
        error_messages = {
            'title': {'required': 'Please tell us what this expense was for.'},
            'expense_date': {'required': 'Please select a date.'},
        }
    def save(self, commit = True):
        instance = super().save(False)
        if self.event is not None and self.update_object is False:
            instance.event = self.event
        if commit:
            instance.save()
        return instance
    
    def clean(self):
        data = super().clean()
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        if len(title) < 3:
            self.add_error('title', 'Title must be at least 3 characters')
        elif len(title) > 50:
            self.add_error('title', 'The title must be no more than 50 characters')
        if len(description) > 5000:
            self.add_error('description', 'The description must be no more than 5000 characters')
        return data

class ParticipantExpenseForm(forms.ModelForm):
    def __init__(self, *args, participant = None, expense = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.participant = participant
        self.expense = expense

    class Meta:
        model = models.ParticipantExpense
        fields = ['share_amount', 'paid_amount', 'description']
        labels = {
            'share_amount': 'Share amount',
            'paid_amount': 'Paid amount',
            'description': 'Comment'
        }
        widgets = {
            'share_amount': forms.TextInput(
                attrs={
                'class': 'js-amount wizard-input-small amount-input-form',
                'placeholder': '0',
            }),
            'paid_amount': forms.TextInput(
                attrs={
                'class': 'js-paid-amount wizard-input-small amount-input-paid',
                'placeholder': '0',
            }),
            'description': forms.Textarea(attrs={
                'class': 'wizard-input-small js-amount-comment hidden mt-3',
                'placeholder': 'Why this amount?',
                'rows':'2'
            })
        }

    def save(self, commit = True):
        instance = super().save(False)
        instance.participant = self.participant
        instance.expense = self.expense

        if commit:
            instance.save()

        return instance
