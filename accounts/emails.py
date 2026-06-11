from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_activation_code_email(user, target_email = None):
    """
    Sends an activation email to the user.
    If USE_FIXED_EMAIL_ACTIVATION_CODE is active, the email sending is bypassed.
    """
    if getattr(settings, 'USE_FIXED_EMAIL_ACTIVATION_CODE', False):
        return None
    
    html = render_to_string('emails/activation_code_email.html', {'user': user})
    text_content = f"Your activation code is: {user.email_active_code}"

    email_message = EmailMultiAlternatives(
        subject = 'Activate Your Email - SplitTrip',
        body = text_content,
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = [target_email]
    )

    email_message.attach_alternative(html, "text/html")
    email_message.send()