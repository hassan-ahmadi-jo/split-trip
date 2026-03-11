from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign_up_page'),
    path('activate/', views.EmailActivationView.as_view(), name='email_activation_page'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]