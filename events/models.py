from django.db import models
from django.db import IntegrityError
import random, string
from accounts.models import User

# Create your models here.
def create_event_code():
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choices(chars, k=7))

class Event(models.Model):
    title = models.CharField(max_length=250, verbose_name='Title')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    code = models.CharField(max_length=7, unique=True, verbose_name='ID')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', verbose_name='creator')

    def save(self, *args, **kwargs):
        if not self.code:
            max_tries = 20
            create_code_try  = 0

            while True:
                self.code = create_event_code()
                try:
                    return super().save(*args, **kwargs)
                except IntegrityError:
                    self.code = None
                    create_code_try += 1

                if create_code_try > max_tries:
                    raise IntegrityError("Unable to generate unique event code after many attempts.")
                
        return super().save(*args, **kwargs)
    
class EventMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships', verbose_name='user')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='memberships', verbose_name='event')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='joined at')
    can_edit_event_info = models.BooleanField(default=False, verbose_name='can edit event information')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='unique_user_event_membership'
            )
        ]

class EventJoinRequest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='join_requests' ,verbose_name='Event')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='join_requests' ,verbose_name='User')
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name='requested at')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='unique_user_event_join_request'
            )
        ]