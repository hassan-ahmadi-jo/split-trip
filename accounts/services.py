from . import models, emails

def create_and_send_email_activation_code(user, target_email = None, generate_code = True):
    if target_email is None:
        target_email = user.email
    
    if generate_code:
        code = models.generate_email_active_code()
        user.email_active_code = code
        user.save(update_fields = ['email_active_code'])

    emails.send_activation_code_email(user, target_email)
