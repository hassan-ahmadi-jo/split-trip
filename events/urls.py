from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name ='home'),
    path('create-event', views.CreateEventView.as_view(), name ='create_event'),
]
