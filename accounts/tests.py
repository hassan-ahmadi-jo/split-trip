from django.test import TestCase
from .models import User
from django.db.utils import IntegrityError

# Create your tests here.

# Model
class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(first_name = 'user1', email = 'test@gmail.com')
        return super().setUp()
    
    def test_username_is_set_from_email(self):
        self.assertEqual(self.user.email, self.user.username)

    def test_is_email_active_default(self):
        self.assertEqual(self.user.is_email_active, False)

    def test_is_email_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(first_name = 'user2', email = 'test@gmail.com')
