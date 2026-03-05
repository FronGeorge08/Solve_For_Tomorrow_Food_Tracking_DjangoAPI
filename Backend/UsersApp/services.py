import secrets
from django.core.mail import send_mail


def generate_verification_code():
    """Generate a secure 6-digit verification code"""
    return str(secrets.randbelow(900000) + 100000)


def send_verification_email(user):
    """Send verification email"""

    subject = "Verify your email"

    message = f"""
Hello {user.username},

Your verification code is:

{user.verification_code}

Enter this code in the application to verify your email.

"""

    from_email = "fron.george09@gmail.com"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)