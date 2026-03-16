from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpensesView.as_view(), name='expenses'),
    path('participants-create/', views.ParticipantsCreateView.as_view(), name='participants_create'),
    path('participants/<int:id>/edit', views.ParticipantsUpdateView.as_view(), name='participants_update'),
    path('participants-list', views.ParticipantsListView.as_view(), name='participants_list'),
    path('participants-delete', views.ParticipantsDeleteView.as_view(), name='participants_delete'),
]