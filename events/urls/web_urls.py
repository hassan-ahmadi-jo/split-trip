from django.urls import path
from ..views import web_views as views

urlpatterns = [
    # --- Event Dashboard
    path('', views.SplitterDashboardView.as_view(), name ='splitter_dashboard'), #splitter_dashboard
    path('events/create/', views.CreateEventView.as_view(), name ='create_event'),
    path('events/', views.EventListView.as_view(), name ='event_list'),

    # --- Event detail
    path('events/<str:event_code>/', views.EventView.as_view(), name ='event'),
    path('events/<str:event_code>/edit/', views.EventUpdateView.as_view(), name ='event_edit'),
    path('events/<str:event_code>/leave/', views.LeaveEventView.as_view(), name ='leave_event'),
    path('events/<str:event_code>/delete/', views.EventDeleteView.as_view(), name ='event_delete'),
    path('events/<str:event_code>/delete/failure/', views.EventDeleteFailure.as_view(), name ='event_delete_failure'),

    # --- Event Temporary
    path('events/<str:event_code>/edit/success/', views.EventUpdateSuccessView.as_view(), name ='event_edit_success'),
    path('events/<str:event_code>/create/success/', views.CreateEventSuccessView.as_view(), name ='create_event_success'),
    path('events/delete-success/', views.EventDeleteSuccess.as_view(), name ='event_delete_success'),


    # --- Membership
    path('members/<int:member_id>/handler/', views.EventMembershipHandlerView.as_view(), name ='event_membership_handler'),
    path('events/<str:event_code>/members/', views.EventMembersListView.as_view(), name ='event_members_list'),
    

    # --- Join Requests
    path('join-requests/', views.JoinRequestListView.as_view(), name ='join_request_list'),
    path('join-requests/create/', views.CreateJoinRequestView.as_view(), name ='create_join_request'),
    path('join-requests/handler/<int:request_id>/', views.JoinRequestHandlerView.as_view(), name ='join_request_handler'),
    path('events/<str:event_code>/join-requests/', views.EventJoinRequestListView.as_view(), name ='event_join_request_list'),


    # --- Join Requests Temporary
    path('join-requests/create/success/<str:event_title>/', views.CreateJoinRequestSuccessView.as_view(), name ='create_join_request_success'),
]
