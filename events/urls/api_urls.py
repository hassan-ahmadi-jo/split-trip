from django.urls import path
from ..views import api_views as view

urlpatterns = [
    path('', view.HomeAPI.as_view()),
    path('create-event/', view.EvantCreateAPI.as_view()),
    path('create-join-request/', view.JoinRequestCreateAPI.as_view()),
    path('events/<str:event_code>/', view.EventAPI.as_view()),
    path('join-request-delete/<int:pk>/', view.JoinRequestDeleteAPI.as_view()),
    path('join-request-accept/<int:pk>/', view.JoinRequestAcceptAPI.as_view()),
    path('membership-delete/<int:pk>/', view.MembershipDeleteAPI.as_view()),
    path('membership-update/<int:pk>/', view.MembershipUpdateAPI.as_view()),
    path('event-list/', view.EventListAPI.as_view()),
    path('join-request-list/', view.UserJoinRequestListAPI.as_view()),
    path('events/<str:event_code>/join-requests/', view.EventJoinRequestListAPI.as_view()),
    path('events/<str:event_code>/members/', view.EventMembersListAPI.as_view()),
]