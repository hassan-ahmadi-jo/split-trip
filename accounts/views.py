from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.contrib.auth import login
from datetime import datetime, timedelta
from django.contrib.auth.views import LoginView
from . import forms, models


# Create your views here.

# Helper function to calculate the retry delay for a user
def calculate_retry_delay(failed_attempts):
    try:
        failed_attempts = int(failed_attempts)
    except:
        return datetime.now() - timedelta(minutes=1)
    failed_limit = 5
    base_penalty_time = 3
    if failed_attempts == 0:
        return datetime.now() - timedelta(minutes=1)
    if failed_attempts % failed_limit == 0:
        penalty_time = base_penalty_time ** int(failed_attempts / failed_limit) # minutes
    else:
        penalty_time = 0 # minutes
    penalty_time -= 1
    return datetime.now() + timedelta(minutes=penalty_time)


class SignUpView(CreateView):
    form_class = forms.SignUpForm
    template_name = 'accounts/sign_up_page.html'
    success_url = reverse_lazy('email_activation_page')
    # to do: check if user is login or not

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
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

            # Check for existing session data. 
            if request.session.get('retry_available_at') and request.session.get('email_activation_failed_attempts'):
                retry_available_at = datetime.fromtimestamp(request.session.get('retry_available_at'))
                
            else:
                self.request.session['email_activation_failed_attempts'] = 0
                self.request.session['retry_available_at'] = (datetime.now() - timedelta(minutes=1)).timestamp() # minutes
                retry_available_at = datetime.now() - timedelta(minutes=1)

            if retry_available_at < datetime.now(): # Check if the user can activate their email.
                # calculate retry delay
                retry_available_at = calculate_retry_delay(request.session.get('email_activation_failed_attempts'))

                # Validate the verification code and update the user’s email activation status. 
                if user.email_active_code == verification_code:
                    user.is_email_active = True
                    user.email_active_code = models.generate_email_active_code()
                    user.save()
                    self.request.session['email_activation_failed_attempts'] = 0
                    # todo: redirect to home page
                elif retry_available_at > datetime.now(): # If the retry delay changes, it will be stored in the session and the user cannot retry for a while.
                    self.request.session['retry_available_at'] = retry_available_at.timestamp()
                    form.add_error('verification_code', 'Too many attempts.')
                    self.request.session['email_activation_failed_attempts'] += 1
                else:
                    form.add_error('verification_code', 'The verification code is incorrect')
                    self.request.session['email_activation_failed_attempts'] += 1

            else: # Return an error if the user has exceeded the retry limit. 
                minutes = int((retry_available_at - datetime.now()).total_seconds() / 60) + 1
                form.add_error('verification_code', f'Too many attempts. Please try again in {minutes} minutes.')
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