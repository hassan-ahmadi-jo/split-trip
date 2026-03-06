from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up_page')
]