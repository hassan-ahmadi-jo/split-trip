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
        