from django.urls import path
from . import views

urlpatterns = [
    # Tracker
    path('', views.ExpensesView.as_view(), name='tracker'), #tracker

    # Participants
    path('participants/', views.ParticipantsListView.as_view(), name='participants_list'),
    path('participants/<int:id>/', views.ParticipantDetailView.as_view(), name='participants_detail'),
    path('participants/<int:id>/update/', views.ParticipantsUpdateView.as_view(), name='participants_update'),
    path('participants/create/', views.ParticipantsCreateView.as_view(), name='participants_create'),
    path('participants/delete/', views.ParticipantsDeleteView.as_view(), name='participants_delete'),

    # Expenses
    path('expenses/', views.ExpensesListView.as_view(), name='expenses_list'),
    path('expenses/<int:expense_id>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:id>/update/', views.ExpensesUpdateView.as_view(), name='expenses_update'),
    path('expenses/<int:expense_id>/delete/', views.ExpensesDeleteView.as_view(), name='expense_delete'),
    path('expenses/create/', views.ExpensesCreateView.as_view(), name='expenses_create'),
    
    # Split payment for a specific expense
    path('expenses/<int:expense_id>/split-payment/', views.SplitPaymentView.as_view(), name='split_payment'),
    path('expenses/<int:expense_id>/split-payment/success/', views.SplitPaymentSuccessView.as_view(), name='split_payment_Success'),

    # Currency
    path('currency/handler/', views.CurrencyHandlerView.as_view(), name='currency_handler'),
    path('currency/create/', views.CurrencyUnitCreateView.as_view(), name='currency_create'),

    # Access Restricted
    path('access-restricted/', views.AccessRestrictedView.as_view(), name='access_restricted'),
]