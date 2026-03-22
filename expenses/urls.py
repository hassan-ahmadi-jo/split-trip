from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpensesView.as_view(), name='dashboard'),
    path('participants-create/', views.ParticipantsCreateView.as_view(), name='participants_create'),
    path('participants/edit/<int:id>/', views.ParticipantsUpdateView.as_view(), name='participants_update'),
    path('participants-list/', views.ParticipantsListView.as_view(), name='participants_list'),
    path('participants-delete/', views.ParticipantsDeleteView.as_view(), name='participants_delete'),
    path('create/', views.ExpensesCreateView.as_view(), name='expenses_create'),
    path('update/<int:id>/', views.ExpensesUpdateView.as_view(), name='expenses_update'),
    path('split-payment/<int:expense_id>/', views.SplitPaymentView.as_view(), name='split_payment'),
    path('split-payment-success/<int:expense_id>/', views.SplitPaymentSuccessView.as_view(), name='split_payment_Success'),
]