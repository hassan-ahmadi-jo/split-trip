from django.test import TestCase
from . import models
from accounts.models import User
from events.models import Event
from django.db.utils import IntegrityError

# Create your tests here.

class ParticipantsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name = 'user', email = 'x@y.com')
        self.event = Event.objects.create(title = 'event', creator = self.user)
        self.participant = models.Participants.objects.create(full_name = 'participant', event = self.event)
        return super().setUp()
    
    def test_participant_exists(self):
        self.assertIsNotNone(self.participant.id)
    
    def test_event_related_name(self):
        event_participants = self.event.participants

        self.assertEqual(event_participants.count(), 1)
        self.assertEqual(event_participants.first(), self.participant)

    def test_full_name_event_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            models.Participants.objects.create(full_name = 'participant', event = self.event)