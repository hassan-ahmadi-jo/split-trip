from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ['id', 'title', 'code', 'creator']

class EventMembershipSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    user = UserSerializer()

    class Meta:
        model = models.EventMembership
        fields = ['user', 'event', 'joined_at', 'can_edit_event_info']

class EventJoinrequestSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    user = UserSerializer()

    class Meta:
        model = models.EventJoinRequest
        fields = ['event', 'user', 'requested_at']

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ['title']

    def validate(self, attrs):
        user = self.context['request'].user
        title = attrs.get('title')
        if user.memberships.filter(event__title__iexact = title).exists():
            raise serializers.ValidationError('You already have an event with this name. Please choose a different name.')
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get('request').user
        event = models.Event.objects.create(
            creator = user,
            **validated_data
        )
        models.EventMembership.objects.create(
            event = event,
            user = user,
            can_edit_event_info = True
        )
        return event

class JoinRequestCreateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, user = None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    event_code = serializers.CharField(write_only = True, max_length = 10)
    class Meta:
        model = models.EventJoinRequest
        fields = ['event_code']

    def validate(self, attrs):
        user = self.user
        event_code = attrs.get('event_code')
        try:
            self.event = models.Event.objects.get(code=event_code)
        except models.Event.DoesNotExist:
            raise serializers.ValidationError("The event code is incorrect")
        
        if user.join_requests.filter(event = self.event).exists():
            raise serializers.ValidationError('You’ve already sent a request to join this event.')
        
        if user.memberships.filter(event = self.event).exists():
            raise serializers.ValidationError('You are already a member of this event.')

        return attrs
        
    def create(self, validated_data):
        return models.EventJoinRequest.objects.create(event = self.event, user = self.user)
    