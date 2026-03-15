from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name ='home'),
    path('create-event/', views.CreateEventView.as_view(), name ='create_event'),
    path('create-join-request/', views.CreateJoinRequestView.as_view(), name ='create_join_request'),
    path('event/<str:event_code>', views.EventView.as_view(), name ='event'),
    path('join-request-handler/<int:request_id>', views.JoinRequestHandlerView.as_view(), name ='join_request_handler'),
    path('event-membership-handler/<int:member_id>', views.EventMembershipHandlerView.as_view(), name ='event_membership_handler'),
    path('event-list', views.EventListView.as_view(), name ='event_list'),
    path('join-request-list', views.JoinRequestListView.as_view(), name ='join_request_list'),
    path('event/<str:event_code>/join-request', views.EventJoinRequestListView.as_view(), name ='event_join_request_list'),
    path('event/<str:event_code>/members', views.EventMembersListView.as_view(), name ='event_members_list'),
    path('create-event-success/<str:event_code>', views.CreateEventSuccessView.as_view(), name ='create_event_success'),
    path('create-join-request-success/<str:event_title>', views.CreateJoinRequestSuccessView.as_view(), name ='create_join_request_success'),
]
