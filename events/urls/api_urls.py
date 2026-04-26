from django.urls import path
from ..views import api_views as view

urlpatterns = [
    path('', view.HomeAPI.as_view())
]