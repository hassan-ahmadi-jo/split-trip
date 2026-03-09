from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.auth.views import LoginView
from . import forms, models


# Create your views here.

class SignUpView(CreateView):
    form_class = forms.SignUpForm
    template_name = 'accounts/sign_up_page.html'
    success_url = reverse_lazy('active_email_page')
    # to do: check if user is login or not

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        # to do:
        # self.request.session['email_activation_failed_attempts'] = 0
        # self.request.session['retry_available_at'] = 0
        return response

class EmailActivationView(View):
    def get(self, request):
        # todo: check if email is active ore not
        # todo: check if user is login or not
        form = forms.EmailActivationForm
        return render(request, 'accounts/email_activation_page.html', {'form': form})
    def post(self, request:HttpRequest):
        # todo: check if email is active ore not
        form = forms.EmailActivationForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data.get('verification_code')
            user = request.user
            if user.email_active_code == verification_code:
                user.is_email_active = True
                user.email_active_code = models.generate_email_active_code()
                user.save()
                # todo: redirect to home page
            else:
                form.add_error('verification_code', 'The verification code is incorrect')
        return render(request, 'accounts/email_activation_page.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    form_class = forms.UserLoginForm
    # todo:
    # next_page = 'home'
    next_page = 'email_activation_page'


# users = models.User.objects.all()
# for user in users:
#     print(user.first_name)
#     print(user.email_active_code)
#     print(user.is_email_active)
#     # user.delete()
#     print('------------------')