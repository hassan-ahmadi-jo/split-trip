from django.urls import path
from ..views import api_views as view

urlpatterns = [
    # --- Event Dashboard
    path('', view.SplitterDashboardAPI.as_view()),
    path('events/create/', view.EvantCreateAPI.as_view()),
    path('events/', view.EventListAPI.as_view()),

    # --- Event detail
    path('events/<str:event_code>/', view.EventAPI.as_view()),
    path('events/<str:event_code>/edit/', view.EventUpdateDeleteAPI.as_view()),

    # --- Membership
    path('members/<int:pk>/delete/', view.MembershipDeleteAPI.as_view()),
    path('members/<int:pk>/update/', view.MembershipUpdateAPI.as_view()),
    path('events/<str:event_code>/members/', view.EventMembersListAPI.as_view()),

    # --- Join Requests
    path('join-requests/', view.UserJoinRequestListAPI.as_view()),
    path('join-requests/create/', view.JoinRequestCreateAPI.as_view()),
    path('join-requests/<int:pk>/delete/', view.JoinRequestDeleteAPI.as_view()),
    path('join-requests/<int:pk>/accept/', view.JoinRequestAcceptAPI.as_view()),
    path('events/<str:event_code>/join-requests/', view.EventJoinRequestListAPI.as_view()),
    
]