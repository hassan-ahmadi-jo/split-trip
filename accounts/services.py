from . import emails, models
import random
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

def generate_email_active_code():
    if settings.USE_FIXED_EMAIL_ACTIVATION_CODE:
        return settings.FIXED_EMAIL_ACTIVATION_CODE
    return str(random.randint(100000, 999999))

def create_and_send_email_activation_code(user, target_email = None, generate_code = True):
    now = timezone.now()

    activation, _ = models.EmailActivation.objects.get_or_create(user = user)
    email_send_available_at = activation.email_send_available_at

    if email_send_available_at > now:
        available_time = email_send_available_at - now
        return int(available_time.total_seconds())
    
    if target_email is None:
        target_email = user.email
    
    if generate_code:
        user.email_active_code = generate_email_active_code()
        user.save(update_fields = ['email_active_code'])

    activation.expires_at = now + timedelta(minutes=settings.EMAIL_ACTIVATION_CODE_EXPIRE_MINUTES)
    activation.email_send_available_at = now + timedelta(minutes=settings.EMAIL_ACTIVATION_RESEND_COOLDOWN_MINUTES)
    activation.save(update_fields=['expires_at', 'email_send_available_at'])

    emails.send_activation_code_email(user, target_email)
    return int(settings.EMAIL_ACTIVATION_RESEND_COOLDOWN_MINUTES * 60)

# Helper function to calculate the retry delay for a user
def calculate_retry_available_at(failed_attempts):
    now = datetime.now()
    try:
        failed_attempts = int(failed_attempts)
    except:
        return now - timedelta(minutes=1)
    failed_limit = 5
    base_penalty_time = 3
    if failed_attempts == 0:
        return now - timedelta(minutes=1)
    if failed_attempts % failed_limit == 0:
        penalty_time = base_penalty_time ** int(failed_attempts / failed_limit) # minutes
    else:
        penalty_time = 0 # minutes
    penalty_time -= 1
    return now + timedelta(minutes=penalty_time)
