from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign_up_page'),
    path('activate/', views.EmailActivationView.as_view(), name='email_activation_page'),
]