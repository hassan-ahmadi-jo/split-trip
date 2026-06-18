from django import forms
from . import models
from accounts.models import User


class ContactMessageForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        max_length=30,
        widget=forms.EmailInput(attrs={
            'class': 'contant-form-email',
            'placeholder': 'you@example.com'
        }),
        error_messages={
            'required': 'This field is required.'
        }
    )

    class Meta:
        model = models.ContactMessage
        fields = ['message']
        labels = {
            'message': 'Message'
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'contant-form-textarea',
                'placeholder': 'Write your message here...'
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
            print('------------')
            print(User.objects.filter(email = email).exists())
            sender.save(update_fields=['is_sender_member'])
        return contact_message