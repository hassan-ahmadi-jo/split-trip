from django import forms
from . import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class ContactMessageForm(forms.ModelForm):
    email = forms.EmailField(
        label= _('Email'),
        max_length=30,
        widget=forms.EmailInput(attrs={
            'class': 'contact-form-email',
            'placeholder': 'you@example.com'
        }),
        error_messages={
            'required': _('This field is required.')
        }
    )

    class Meta:
        model = models.ContactMessage
        fields = ['message']
        labels = {
            'message': _('Message')
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'contact-form-textarea',
                'placeholder': _('Write your message here...')
            })
        }
    
    def save(self, commit = True):
        contact_message = super().save(False)
        if commit:
            email = self.cleaned_data.get('email')
            sender, _ = models.ContactSender.objects.get_or_create(email = email)
            contact_message.sender = sender
            contact_message.save()
            sender.is_sender_member = User.objects.filter(email = email).exists()
            sender.save(update_fields=['is_sender_member'])
        return contact_message