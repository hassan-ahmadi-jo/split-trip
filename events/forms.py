from django import forms
from . import models

class CreateEventForm(forms.ModelForm):
    def __init__(self, *args, user=None, update_form = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.update_form = update_form
    class Meta:
        model = models.Event
        fields = ['title']

        labels = {
            'title':'Event title'
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your title'
            })
        }

        error_messages = {
            'title': {
                'required': 'This field is required.',
            }
        }
    def clean_title(self):
        title = self.cleaned_data.get('title')
        user = self.user
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters.')
        elif len(title) > 250:
            raise forms.ValidationError('The title must not exceed 250 characters.')
        if user and user.memberships.filter(event__title__iexact = title).exists():
            raise forms.ValidationError('You already have an event with this name. Please choose a different name.')
        
        return title
    
    def save(self, commit = True):
        event = super().save()
        if commit:
            event.save()
            if not self.update_form:
                models.EventMembership.objects.create(
                    event=event,
                    user = self.user,
                    can_edit_event_info = True
                    )
        return event
    
class CreateJoinRequestForm(forms.Form):
    event_code = forms.CharField(
        label='Event code:',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the event code'
        }),
        error_messages={
            'required': 'This field is required.'
        }
    )
