from django.urls import path
from ..views import api_views as view

urlpatterns = [
    path('', view.HomeAPI.as_view()),
    path('create-event/', view.EvantCreateAPI.as_view()),
    path('create-join-request/', view.JoinRequestCreateAPI.as_view())
]