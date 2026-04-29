from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .. import models, serializers
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from django.db import transaction

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

class JoinRequestDeleteAPI(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventJoinrequestSerializer
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        user = self.request.user
        join_request = get_object_or_404(models.EventJoinRequest.objects.select_related('user', 'event', 'event__creator'), id = pk)
        if join_request.user == user or join_request.event.creator == user:
            return join_request
        else:
            raise NotFound()

class JoinRequestAcceptAPI(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def add_user_to_event(self, join_request):
        models.EventMembership.objects.get_or_create(
            user = join_request.user,
            event = join_request.event
        )
        join_request.delete()

    def post(self, request: Request, pk):
        user = request.user
        join_request = get_object_or_404(models.EventJoinRequest.objects.select_related('user', 'event', 'event__creator'), id = pk)
        if join_request.event.creator == user:
            self.add_user_to_event(join_request)
            return Response({'ok': True, 'message': 'Join request accepted success'})
        else:
            raise NotFound()

class MembershipDeleteAPI(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get_object(self):
        user = self.request.user
        id = self.kwargs.get('pk')
        membership = get_object_or_404(models.EventMembership.objects.select_related('user', 'event', 'event__creator'), id = id)
        if user in (membership.event.creator, membership.user) and membership.event.creator != membership.user:
            return membership
        raise NotFound()

class MembershipUpdateAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventMembershipUpdateSerializer
    
    def get_object(self):
        user = self.request.user
        id = self.kwargs.get('pk')
        membership = get_object_or_404(models.EventMembership.objects.select_related('user', 'event', 'event__creator'), id = id)
        if user == membership.event.creator and membership.user != user:
            return membership
        raise NotFound()

class EventListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventMembershipSerializer

    def get_queryset(self):
        user = self.request.user
        return user.memberships.select_related('event', 'event__creator').order_by('-joined_at')
    
class UserJoinRequestListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventJoinrequestSerializer

    def get_queryset(self):
        user = self.request.user
        return user.join_requests.select_related('event', 'event__creator').order_by('-requested_at')
    
class EventJoinRequestListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventJoinrequestSerializer

    def get_queryset(self):
        event_code = self.kwargs.get('event_code')
        user = self.request.user
        event = get_object_or_404(models.Event.objects.select_related('creator'), code = event_code, creator = user)
        return event.join_requests.select_related('user', 'event__creator').order_by('-requested_at')

class EventMembersListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.EventMembershipSerializer

    def get_queryset(self):
        event_code = self.kwargs.get('event_code')
        user = self.request.user
        event = get_object_or_404(models.Event.objects.select_related('creator'), code = event_code, creator = user)
        return event.memberships.select_related('user', 'event__creator').order_by('joined_at')