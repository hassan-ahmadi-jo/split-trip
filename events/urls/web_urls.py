from django.urls import path
from ..views import web_views as views

urlpatterns = [
    path('', views.HomeView.as_view(), name ='home'),
    path('create-event/', views.CreateEventView.as_view(), name ='create_event'),
    path('create-join-request/', views.CreateJoinRequestView.as_view(), name ='create_join_request'),
    path('events/<str:event_code>/', views.EventView.as_view(), name ='event'),
    path('join-request-handler/<int:request_id>/', views.JoinRequestHandlerView.as_view(), name ='join_request_handler'),
    path('event-membership-handler/<int:member_id>/', views.EventMembershipHandlerView.as_view(), name ='event_membership_handler'),
    path('event-list/', views.EventListView.as_view(), name ='event_list'),
    path('join-request-list/', views.JoinRequestListView.as_view(), name ='join_request_list'),
    path('events/<str:event_code>/join-requests/', views.EventJoinRequestListView.as_view(), name ='event_join_request_list'),
    path('events/<str:event_code>/members/', views.EventMembersListView.as_view(), name ='event_members_list'),
    path('create-event-success/<str:event_code>/', views.CreateEventSuccessView.as_view(), name ='create_event_success'),
    path('create-join-request-success/<str:event_title>/', views.CreateJoinRequestSuccessView.as_view(), name ='create_join_request_success'),
    path('event-edit/<str:event_code>/', views.EventUpdateView.as_view(), name ='event_edit'),
    path('event-edit-success/<str:event_code>/', views.EventUpdateSuccessView.as_view(), name ='event_edit_success'),
    path('event-delete/<str:event_code>/', views.EventDeleteView.as_view(), name ='event_delete'),
    path('event-delete-success/', views.EventDeleteSuccess.as_view(), name ='event_delete_success'),
    path('event-delete-failure/<str:event_code>/', views.EventDeleteFailure.as_view(), name ='event_delete_failure'),
    path('leave-event/<str:event_code>/', views.LeaveEventView.as_view(), name ='leave_event'),
]
