from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard', views.ExpensesView.as_view(), name='dashboard'),

    # Participants
    path('participants/create/', views.ParticipantsCreateView.as_view(), name='participants_create'),
    path('participants/<int:id>/update/', views.ParticipantsUpdateView.as_view(), name='participants_update'),
    path('participants/list/', views.ParticipantsListView.as_view(), name='participants_list'),
    path('participants/delete/', views.ParticipantsDeleteView.as_view(), name='participants_delete'),
    path('participants/<int:id>/', views.ParticipantDetailView.as_view(), name='participants_detail'),

    # Expenses
    path('expenses/create/', views.ExpensesCreateView.as_view(), name='expenses_create'),
    path('expenses/<int:id>/update/', views.ExpensesUpdateView.as_view(), name='expenses_update'),
    path('expenses/list/', views.ExpensesListView.as_view(), name='expenses_list'),
    path('expenses/<int:expense_id>/delete/', views.EpensesDeleteView.as_view(), name='expense_delete'),
    path('expenses/<int:expense_id>/', views.ExpenseDetailView.as_view(), name='expense_detail'),

    # Split payment for a specific expense
    path('expenses/<int:expense_id>/split-payment/', views.SplitPaymentView.as_view(), name='split_payment'),
    path('expenses/<int:expense_id>/split-payment-success/', views.SplitPaymentSuccessView.as_view(), name='split_payment_Success'),

    # Currency
    path('currency/', views.CurrencyHandlerView.as_view(), name='currency_handler'),
    path('currency/create/', views.CurrencyUnitCreateView.as_view(), name='currency_create'),

    # Access Restricted
    path('access-restricted', views.AccessRestrictedView.as_view(), name='access_restricted'),
]