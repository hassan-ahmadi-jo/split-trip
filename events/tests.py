from django.test import TestCase
from django.test import TransactionTestCase
from accounts.models import User
from . import models
from django.db.utils import IntegrityError
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

class EventMembershipModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name = 'user', email = 'user@y.com')
        self.event = models.Event.objects.create(title = 'event', creator = self.user)
        self.event_membership = models.EventMembership.objects.create(user = self.user, event = self.event)
        return super().setUp()
    
    def test_event_membership_exists(self):
        self.assertIsNotNone(self.event_membership.id)
    
    def test_user_event_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            models.EventMembership.objects.create(event = self.event, user = self.user)

    def test_related_name_user_membership(self):
        memberships = self.user.memberships.all()

        self.assertEqual(memberships.count(), 1)
        self.assertEqual(memberships.first(), self.event_membership)

    def test_related_name_event_membership(self):
        memberships = self.event.memberships.all()
        
        self.assertEqual(memberships.count(), 1)
        self.assertEqual(memberships.first(), self.event_membership)

class EventJoinRequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name = 'user', email = 'user@y.com')
        self.event = models.Event.objects.create(title = 'event', creator = self.user)
        self.join_request = models.EventJoinRequest.objects.create(user = self.user, event = self.event)
        return super().setUp()
    
    def test_join_request_exists(self):
        self.assertIsNotNone(self.join_request.id)
    
    def test_user_event_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            models.EventJoinRequest.objects.create(event = self.event, user = self.user)

    def test_related_name_user_join_request(self):
        join_requests = self.user.join_requests.all()

        self.assertEqual(join_requests.count(), 1)
        self.assertEqual(join_requests.first(), self.join_request)

    def test_related_name_event_join_request(self):
        join_requests = self.event.join_requests.all()
        
        self.assertEqual(join_requests.count(), 1)
        self.assertEqual(join_requests.first(), self.join_request)