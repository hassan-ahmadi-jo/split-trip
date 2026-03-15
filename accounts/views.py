from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.contrib.auth import login
from datetime import datetime, timedelta
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import UserPassesTestMixin
from . import forms, models

# Create your views here.

# Helper function to calculate the retry delay for a user
def calculate_retry_available_at(failed_attempts):
    now = datetime.now()
    try:
        failed_attempts = int(failed_attempts)
    except:
        return now - timedelta(minutes=1)
    failed_limit = 5
    base_penalty_time = 3
    if failed_attempts == 0:
        return now - timedelta(minutes=1)
    if failed_attempts % failed_limit == 0:
        penalty_time = base_penalty_time ** int(failed_attempts / failed_limit) # minutes
    else:
        penalty_time = 0 # minutes
    penalty_time -= 1
    return now + timedelta(minutes=penalty_time)


class SignUpView(UserPassesTestMixin, CreateView):
    form_class = forms.SignUpForm
    template_name = 'accounts/sign_up_page.html'
    success_url = reverse_lazy('email_activation_page') # todo: reverse to home

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        self.request.session['pending_verification_user_id'] = user.id
        return response

class EmailActivationView(View):
    """
    Email activation contract:
    - If user is authenticated: redirect home.
    - Requires `pending_verification_user_id` in session; otherwise redirect to login.
    - On valid code: mark email verified, log user in, clear pending session key, redirect home.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        if request.session.get('pending_verification_user_id') is None:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = forms.EmailActivationForm()
        user = models.User.objects.filter(id = request.session.get('pending_verification_user_id')).first()
        if user is None:
            return redirect('login')
        user_email = user.email
        return render(request, 'accounts/email_activation_page.html', {'form': form, 'user_email': user_email})
    
    def post(self, request:HttpRequest):
        form = forms.EmailActivationForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/email_activation_page.html', {'form': form})
        

        verification_code = form.cleaned_data.get('verification_code')
        user = models.User.objects.filter(id = request.session.get('pending_verification_user_id')).first()
        if user is None:
            return redirect('login')
        now = datetime.now()

        # Check for existing session data for the activation code retry delay.
        retry_ts = request.session.get('retry_available_at')
        failed_attempts = request.session.get('email_activation_failed_attempts')
        if retry_ts is not None and failed_attempts is not None:
            retry_available_at = datetime.fromtimestamp(retry_ts)
            
        else:
            self.request.session['email_activation_failed_attempts'] = 0
            self.request.session['retry_available_at'] = (now - timedelta(minutes=1)).timestamp() # minutes
            retry_available_at = now - timedelta(minutes=1)

        if retry_available_at < now: # Check if the user can activate their email.
            retry_available_at = calculate_retry_available_at(request.session.get('email_activation_failed_attempts'))

            # If the activation code is valid, activate the user's email, log them in, and redirect to the home page.
            if user.email_active_code == verification_code:
                request.session.pop('pending_verification_user_id', None)
                request.session.pop('retry_available_at', None)
                request.session.pop('email_activation_failed_attempts', None)

                user.is_email_active = True
                user.email_active_code = models.generate_email_active_code()
                user.save()

                login(request, user)
                return redirect('home')
                
            elif retry_available_at > now: # If the retry delay changes, it will be stored in the session and the user cannot retry for a while.
                self.request.session['retry_available_at'] = retry_available_at.timestamp()
                form.add_error('verification_code', 'Too many attempts.')
                self.request.session['email_activation_failed_attempts'] += 1
            else:
                form.add_error('verification_code', 'The verification code is incorrect')
                self.request.session['email_activation_failed_attempts'] += 1
        else: # Return an error if the user has exceeded the retry limit. 
            minutes = int((retry_available_at - now).total_seconds() / 60) + 1
            form.add_error('verification_code', f'Too many attempts. Please try again in {minutes} minutes.')
        return render(request, 'accounts/email_activation_page.html', {'form': form})

class UserLoginView(UserPassesTestMixin ,auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    form_class = forms.UserLoginForm
    next_page = 'home'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_email_active:
            login(self.request, form.get_user())
            return redirect(self.get_success_url())
        self.request.session['pending_verification_user_id'] = user.id
        return redirect('email_activation_page')
    
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('home')

class PasswordResetView(UserPassesTestMixin, auth_views.PasswordResetView):
    # todo: user login
    template_name = 'accounts/password_reset.html'
    email_template_name = "registration/password_reset_email.text"
    form_class = forms.PasswordResetForm

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('home')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(UserPassesTestMixin, auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = forms.PasswordResetConfirmForm

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('home')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


users = models.User.objects.all()
for user in users:
    print(user.first_name)
    print(user.email_active_code)
    print(user.is_email_active)
    # user.delete()
    print('------------------')