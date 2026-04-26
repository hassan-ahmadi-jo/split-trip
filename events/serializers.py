from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer


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
