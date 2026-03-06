from django import forms
from . import models

class SignUpForm(forms.ModelForm):
    repeat_password = forms.CharField(
        label='Repeat the password:',
        widget=forms.PasswordInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Repeat password'
            }))

    class Meta:
        model = models.User
        fields = ['first_name', 'email', 'password']

        labels = {
            'first_name': 'Name:',
            'email': 'Email:',
            'password': 'Password:'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }

        error_messages = {
            'first_name': {'required': 'This field is required.'},
            'email': {'required': 'This field is required.'},
            'password': {'required': 'This field is required.'},
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        name = cleaned_data.get('first_name')
        if len(name) < 3:
            self.add_error('first_name', 'Name must be at least 3 characters')
        elif len(password) < 6:
            self.add_error('password', 'Password must be at least 6 characters')
        elif password != repeat_password:
            self.add_error('repeat_password', 'The password and the repeat password do not match.')
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.email_active_code = models.generate_email_active_code()
        if commit:
            user.save()
        return user