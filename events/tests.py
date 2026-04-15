from django.test import TestCase
from django.test import TransactionTestCase
from accounts.models import User
from . import models
import random

# Create your tests here.

class EventModelTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create(first_name = 'user', email = 'x@y.com')
        self.event = models.Event.objects.create(title='event_1', creator = self.user)
        return super().setUp()
    
    def test_event_exists(self):
        self.assertIsNotNone(self.event.id)

    def test_event_code_is_generated(self):
        self.assertEqual(len(self.event.code), 7)

    def test_event_code_is_unique(self):
        event2 = models.Event.objects.create(title='event_2', creator = self.user)
        self.assertNotEqual(self.event.code, event2.code)
    
    def test_event_code_collision_is_resolved(self):
        def create_event_code():
            from random import randint
            code = str(randint(0, 1))
            return code
        try:
            real_create_event_code = models.create_event_code
            models.create_event_code = create_event_code
            event3 = models.Event.objects.create(title='event_3', creator = self.user)
            event4 = models.Event.objects.create(title='event_4', creator = self.user)
            self.assertNotEqual(event3.code, event4.code)
        finally:
            models.create_event_code = real_create_event_code