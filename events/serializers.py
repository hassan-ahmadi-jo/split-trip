from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer
from django.db import transaction


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
