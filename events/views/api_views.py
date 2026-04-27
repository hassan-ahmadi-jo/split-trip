from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .. import models, serializers
from django.shortcuts import get_object_or_404

class HomeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        user = request.user
        memberships = user.memberships.all().order_by('-joined_at')[:6]
        join_requests = user.join_requests.all().order_by('-requested_at')[:4]

        serializer_memberships = serializers.EventMembershipSerializer(memberships, many = True)
        serializer_join_requests = serializers.EventJoinrequestSerializer(join_requests, many = True)

        return Response({'memberships': serializer_memberships.data, 'join_requests': serializer_join_requests.data}, status = status.HTTP_200_OK)

class EvantCreateAPI(CreateAPIView):
    serializer_class = serializers.EventCreateSerializer
    permission_classes = [IsAuthenticated]

class JoinRequestCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.JoinRequestCreateSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['user'] = self.request.user
        return super().get_serializer(*args, **kwargs)

class EventAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, event_code):
        user = request.user
        membership = get_object_or_404(user.memberships.select_related('event'), event__code = event_code)
        event = membership.event
        membership_serializer = serializers.EventMembershipSerializer(membership)
        context = {'membership': membership_serializer.data}
        if event.creator == user:
            join_requests = models.EventJoinRequest.objects.select_related('user').filter(event = event).order_by('-requested_at')[:4]
            members_list = models.EventMembership.objects.select_related('user').filter(event = event).order_by('joined_at')[:6]
            join_requests_serializer = serializers.EventJoinrequestSerializer(join_requests, many = True)
            members_list_serializer = serializers.EventMembershipSerializer(members_list, many = True)
            context['join_requests'] = join_requests_serializer.data
            context['members_list'] = members_list_serializer.data
        return Response(context, status=status.HTTP_200_OK)
