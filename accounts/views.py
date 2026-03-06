from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . import forms

# Create your views here.

class SignUpView(CreateView):
    form_class = forms.SignUpForm
    template_name = 'accounts/sign_up_page.html'
    success_url = reverse_lazy('sign_up_page')

from . import models
users = models.User.objects.all()
for user in users:
    print(user.first_name)
    print(user.email_active_code)
    print('------------------')