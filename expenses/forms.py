from django import forms
from . import models

class ParticipantsForm(forms.ModelForm):
    def __init__(self, event = None, update_object = False, *args, **kwargs):
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
            raise forms.ValidationError('The name must be at least 5 characters.')
        elif len(data) > 20:
            raise forms.ValidationError('The name must be no more than 20 characters.')
        elif event and event.participants.filter(full_name__iexact=data).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This participant already exists.')
        return data
    
    def save(self, commit = True):
        form = super().save(False)
        if self.event is not None and self.update_object is not False:
            form.event = self.event
        if commit:
            form.save()
        return form

class ExpensesForm(forms.ModelForm):
    def __init__(self, event = None, update_object = False, *args, **kwargs):
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
        form = super().save(False)
        if self.event is not None and self.update_object is False:
            form.event = self.event
        if commit:
            form.save()
    
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

